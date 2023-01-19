from odoo import models, fields, api, _
from odoo import models, fields, api, _
import logging

logger = logging.getLogger(__name__)
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_surface = fields.Float(string='Product surface')

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    original_mo = fields.Many2one('mrp.production', string='Original MO', copy=False)
    raw_product_processing = fields.Boolean(string='Raw product processing', default=False)
    product_manufactured_ids = fields.One2many(
        comodel_name='product.manufactured',
        inverse_name='mo_id',
        string='Products Manufactured',
        copy=False
    )

# Model used to record possible outcomes from each BOM reported in the wizard
class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    outcome_ids = fields.Many2many('product.product', string='Possible Outcomes')
    base_ripping = fields.Boolean(string='Base ripping', default=False)
    allocation_output_1 = fields.Float('Percentage allocated to output 1',default="0.8")
    allocation_output_2 = fields.Float('Percentage allocated to output 2',default="0.2")

class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    
#   Add a new status = To Close
    state = fields.Selection (selection_add=[('close','To Close'),('cancel',)])
    
#   Add a boolean, related product_id.x_studio_cap_process
    is_a_process = fields.Boolean(string="Is a process ?", related='product_id.x_studio_cap_process')
    
#   Complete production action
    def do_proc_finish(self):
        # 1 - Stop the timer
        super().button_finish()
        # 2 - Changer le statut du work order
        self.state = 'close'
        # 3 - Fermer la vue tablet
        
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.production_id.id
        }
        
        # return{
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'mrp.workorder',
        #     'view_mode': 'tree',
        #     'target': 'current',
        #     'context':{'search_default_ready': True, 'search_default_progress': True, 'search_default_pending': True}
        # }
    
    def do_finish(self):
        product_list = []
        # outcome_list = self.production_id.bom_id.outcome_ids
        outcome_list = self.production_id.x_studio_expected_outcomes

        for product in outcome_list:
            product_line = self.env['product.manufactured'].create({
                'product_id': product.x_studio_product.id,
                'quantity': 0,
            })
            product_list.append(product_line.id)

        wizard = self.env['mrp.wizard'].create({
            'processed_mo': self.production_id.id,
            'processed_wo': self.id,
            'product_ids': [(6, 0, product_list)]
        })
        res_id = wizard.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.wizard',
            'view_mode': 'form',
            'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_view_form').id, 'form']],
            'target': 'new',
            'res_id': res_id,
        }


# Model used to record quantities created of each product in the wizard
class ProductManufactured(models.Model):
    _name = 'product.manufactured'

    product_id = fields.Many2one('product.product', string='Product', copy=False)
    quantity = fields.Float(string='Quantity made', default=0, copy=False)
    mo_id = fields.Many2one('mrp.production', string='Manufacture Order', copy=False)
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,record.product_id.name))
        return result


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    error_margin = fields.Float(string="Error margin", default=0)

class MrpWizard(models.Model):
    
    _name = 'mrp.wizard'

    name = fields.Char(string='Name', default='Products manufactured during WO :', readonly=True)
    processed_mo = fields.Many2one('mrp.production', string='Manufacturing order', readonly=True)
    processed_wo = fields.Many2one('mrp.workorder', string='Workorder record', readonly=True)
    product_ids = fields.Many2many('product.manufactured', 'product_wo_wizard_relationship',
                                   string='Products manufactured')
    product_selection = fields.Many2one('product.product', string='Product')
    product_quantity = fields.Float(string='Quantity')

    def finishProduction(self):
        for product in self.product_ids:
            if product.quantity > 0:
                if any(self.processed_mo.product_manufactured_ids.filtered(lambda x: x.product_id == product.product_id)):
                    self.processed_mo.product_manufactured_ids.filtered(lambda x: x.product_id == product.product_id)['quantity'] += product.quantity
                    product.unlink()
                else:
                    product['mo_id'] = self.processed_mo.id
            else:
                product.unlink()
        return self.processed_wo.do_proc_finish()


class StockMove(models.Model):
    _inherit = "stock.move"

    def _set_product_qty(self):
        """ The meaning of product_qty field changed lately and is now a functional field computing the quantity
        in the default product UoM. This code has been added to raise an error if a write is made given a value
        for `product_qty`, where the same write should set the `product_uom_qty` field instead, in order to
        detect errors. """
        return True