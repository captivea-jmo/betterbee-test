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

    original_mo = fields.Many2one('mrp.production', string='Original MO')
    raw_product_processing = fields.Boolean(string='Raw product processing', default=False)


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
        self.state = 'close'
        
        # 2 - Changer le statut du work order
        
        # 3 - Fermer la vue tablet
        
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.workorder',
            'view_mode': 'tree',
            'target': 'current',
            'context':{'search_default_ready': True, 'search_default_progress': True, 'search_default_pending': True}
        }

    #Creating a function to create a manufacturing order to convert Processed item (process ft²) into a finished product
    def createManufacturingOrderWithStockMoves(self,processed_mo,product_manufactured,product_uom_qty,quantity_done ):
        
        picking_type = self.env['stock.picking.type'].search([('name', '=', 'Manufacturing')], limit=1)

#             TPE : try to fix    
        manuf_order = self.env['mrp.production'].create({
            'company_id': processed_mo.company_id.id,
            'consumption': 'flexible',
            'date_planned_start': processed_mo.date_planned_start,
            'location_dest_id': processed_mo.location_dest_id.id,
            'location_src_id': processed_mo.location_src_id.id,
            'picking_type_id': processed_mo.picking_type_id.id,
            'product_id': product_manufactured.id,
            'product_qty': product_uom_qty,
            'qty_producing': quantity_done,
            'product_uom_id': product_manufactured.uom_id.id,
            'original_mo': processed_mo.original_mo.id,
        })
        
        # Create a manufacturing order
#         manuf_order = self.env['mrp.production'].create({
#             'company_id': self.processed_mo.company_id.id,
#             'consumption': 'flexible',
#             'date_planned_start': self.processed_mo.date_planned_start,
#             'location_dest_id': self.processed_mo.location_dest_id.id,
#             'location_src_id': self.processed_mo.location_src_id.id,
#             'picking_type_id': self.processed_mo.picking_type_id.id,
#             'product_id': product_manufactured.product_id.id,
#             'product_qty': product_manufactured.quantity,
#             'qty_producing': product_manufactured.quantity,
#             'product_uom_id': product_manufactured.product_id.uom_id.id,
#             'original_mo': self.processed_mo.id,
#         })

        # Create 2 Stock Moves,
        # 1 move for Consumable FROM WH/Stock TO Virtual/Production
        # 1 move for finished good FROM Virtual/Prod TO WH/Stock

        warehouse_location = self.env['stock.location'].search(
            [('name', '=', 'Stock'), ('company_id', '=', self.env.company.id)], limit=1)
        production_location = self.env['stock.location'].search(
            [('name', '=', 'Production'), ('company_id', '=', self.env.company.id)], limit=1)
        name = manuf_order.name
        processed_product = self.env['product.product'].search([('name', '=', 'Process foot²')], limit=1)
        
#             TPE : try to fix   
        stock_move_processed_product = self.env['stock.move'].create({
            'company_id': processed_mo.company_id.id,
            'date': processed_mo.date_planned_start,
            'location_dest_id': production_location.id,
            'location_id': warehouse_location.id,
            'name': name,
            'procure_method': 'make_to_stock',
            'product_id': processed_product.id,
            'product_uom': processed_product.uom_id.id,
            'product_uom_qty': product_uom_qty, 
            'quantity_done': quantity_done, 
            'raw_material_production_id': manuf_order.id,
            'origin': manuf_order.name,
        })

        stock_move_final_product = self.env['stock.move'].create({
            'company_id': processed_mo.company_id.id,
            'date': processed_mo.date_planned_start,
            'location_dest_id': warehouse_location.id,
            'location_id': production_location.id,
            'name': name,
            'procure_method': 'make_to_stock',
            'product_id': product_manufactured.id,
            'product_uom': product_manufactured.uom_id.id,
            'production_id': manuf_order.id,
            'product_uom_qty': product_uom_qty,
            'quantity_done': quantity_done,
            'picking_type_id': picking_type.id,
            'origin': manuf_order.name,
            'reference':'Final stock move',
        })

        #Moving process ft² to Virtual/Production
#         stock_move_processed_product = self.env['stock.move'].create({
#             'company_id': self.processed_mo.company_id.id,
#             'date': self.processed_mo.date_planned_start,
#             'location_dest_id': production_location.id,
#             'location_id': warehouse_location.id,
#             'name': name,
#             'procure_method': 'make_to_stock',
#             'product_id': processed_product.id,
#             'product_uom': processed_product.uom_id.id,
# #                 'product_uom_qty': product_manufactured.quantity + lost_surface,
# #                 'quantity_done': product_manufactured.quantity + lost_surface,
#             'product_uom_qty': product_uom_qty, # round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
#             'quantity_done': quantity_done, #round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
#             'raw_material_production_id': manuf_order.id,
#             'origin': manuf_order.name,
#         })

#         #Moving final product to WH/Stock
#         stock_move_final_product = self.env['stock.move'].create({
#             'company_id': self.processed_mo.company_id.id,
#             'date': self.processed_mo.date_planned_start,
#             'location_dest_id': warehouse_location.id,
#             'location_id': production_location.id,
#             'name': name,
#             'procure_method': 'make_to_stock',
#             'product_id': product_manufactured.product_id.id,
#             'product_uom': product_manufactured.product_id.uom_id.id,
#             'production_id': manuf_order.id,
#             # 'product_uom_qty': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
#             # 'quantity_done': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
#             'product_uom_qty': product_uom_qty, # product_manufactured.quantity,
#             'quantity_done': quantity_done, #product_manufactured.quantity,
#             'picking_type_id': picking_type.id,
#             'origin': manuf_order.name,
#             'reference':'Final stock move',
#         })

        manuf_order.action_confirm()
        manuf_order.button_mark_done()

        return True


#     def do_finish(self):
#         #Base ripping logic - Simplifies the popup and only uses 2 items as output, ripped and drop
#         if self.production_id.bom_id.base_ripping and not self._context.get('no_start_next'):
            
#             total_surface_used = 0 
#             outcome_product_id_1 = self.production_id.bom_id.outcome_ids[0]
#             outcome_product_id_2 = self.production_id.bom_id.outcome_ids[1]
#             allocation_outcome_1 = self.production_id.bom_id.allocation_output_1
#             allocation_outcome_2 = self.production_id.bom_id.allocation_output_2
            
# #             TPE : try to fix
#             processed_mo = self.production_id.workorder_ids[0].production_id

#             for move in self.move_raw_ids:
#                 total_surface_used = total_surface_used + round(move.product_uom_qty * move.product_id.product_surface, 2)
                
# #             TPE : try to fix
#             #Creating MO and Stock moves for output 1 
# #             self.createManufacturingOrderWithStockMoves(self.processed_mo,outcome_product_id_1.id,round((total_surface_used*allocation_outcome_1),2),round((total_surface_used*allocation_outcome_1),2))
#             self.createManufacturingOrderWithStockMoves(processed_mo,outcome_product_id_1,round((total_surface_used*allocation_outcome_1),2),round((total_surface_used*allocation_outcome_1),2))

#             #Creating MO and Stock moves for output 2 
# #             self.createManufacturingOrderWithStockMoves(self.processed_mo,outcome_product_id_2.id,round((total_surface_used*allocation_outcome_2),2),round((total_surface_used*allocation_outcome_2),2))
#             self.createManufacturingOrderWithStockMoves(processed_mo,outcome_product_id_2,round((total_surface_used*allocation_outcome_2),2),round((total_surface_used*allocation_outcome_2),2))
            
# #             if self._context.get('no_start_next'):
# #                 raise UserError(self._context.get('no_start_next'))

#             action = self.with_context(no_start_next=True).do_finish()
            
            
#             try:
#                 with self.env.cr.savepoint():
# #                     res = self.button_mark_done()
#                     res = processed_mo.button_mark_done()
#                     if res is not True:
#                         res['context'] = dict(res['context'], from_workorder=True)
#                         return res
#             except (UserError, ValidationError) as e:
#                 # log next activity on MO with error message
#                 self.activity_schedule(
#                     'mail.mail_activity_data_warning',
#                     note=e.name,
# #                     summary=('The %s could not be closed') % (self.processed_mo.name),
#                     summary=('The %s could not be closed') % (processed_mo.name),
#                     user_id = self.env.user.id)

#             return action


#         #Raw material popup display
#         if self.production_id.raw_product_processing:
#             product_list = []
#             wizard = self.env['mrp.wizard'].search([('processed_mo', '=', self.production_id.id)], limit=1)
#             if len(wizard) > 0:
#                 res_id = wizard.id
#             else:
#                 outcome_list = self.production_id.bom_id.outcome_ids

#                 for product in outcome_list:
#                     product_line = self.env['product.manufactured'].create({
#                         'product_id': product.id,
#                         'quantity': 0,
#                     })
#                     product_list.append(product_line.id)

#                 wizard = self.env['mrp.wizard'].create({
#                     'processed_mo': self.production_id.id,
#                     'product_ids': [(6, 0, product_list)]
#                 })
#                 res_id = wizard.id

#             context = {
#                 'default_processed_mo': self.production_id.id,
#                 'default_processed_wo': self.id,
#                 # 'default_product_ids': [(6, 0, product_list)],
#             }
#             return {
#                 'type': 'ir.actions.act_window',
#                 'res_model': 'mrp.wizard',
#                 'view_mode': 'form',
#                 'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_view_form').id, 'form']],
#                 'context': context,
#                 'target': 'new',
#                 'res_id': res_id,
#             }
#         else:
#             return super().do_finish()


# Model used to record quantities created of each product in the wizard
class ProductManufactured(models.Model):
    _name = 'product.manufactured'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity made', default=0)
    
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
    
    primary_output = fields.Many2one('product.manufactured', string='Primary Output', domain="[('id', 'in', product_ids)]")
    secondary_output = fields.Many2one('product.manufactured', string='Secondary Output', domain="[('id', 'in', product_ids)]")
    
    def turnProcessedIntoProductsStep1(self):
        product_list = []
        product_qty = self.processed_mo.product_qty
        coef_primary_output = self.processed_mo.bom_id.allocation_output_1
        surface_primary_output = self.processed_mo.bom_id.outcome_ids.filtered(lambda prod: prod.id == self.primary_output.product_id.id).x_studio_outcome_surface
        product_line_primary = self.env['product.manufactured'].create({
                    'product_id': self.primary_output.product_id.id,
                    'quantity': round(product_qty * surface_primary_output * coef_primary_output,2),
                })
        product_list.append(product_line_primary.id)
        
        coef_secondary_output = self.processed_mo.bom_id.allocation_output_2
        surface_secondary_output = self.processed_mo.bom_id.outcome_ids.filtered(lambda prod: prod.id == self.secondary_output.product_id.id).x_studio_outcome_surface
        product_line_secondary = self.env['product.manufactured'].create({
                    'product_id': self.secondary_output.product_id.id,
                    'quantity': round(product_qty * surface_secondary_output * coef_secondary_output,2),
                })
        product_list.append(product_line_secondary.id)
        self.write({
            'product_ids': [(6, 0, product_list)]
        })
        return self.turnProcessedIntoProducts()
        
    
    def resetToPossibleOutcome(self):
        self._compute_bom_outcome(False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.wizard',
            'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_view_form').id, 'form']],
            'target': 'new',
            'res_id': self.id,
        }

    def _compute_bom_outcome(self, return_value=True):
        for record in self:
            product_list = []
            outcome_list = record.processed_mo.bom_id.outcome_ids

            for product in outcome_list:
                product_line = record.env['product.manufactured'].create({
                    'product_id': product.id,
                    'quantity': 0,
                })
                product_list.append(product_line.id)
            record.write({
                'product_ids': [(6, 0, product_list)]
            })
            if return_value:
                return True

    def addProductToList(self):

        line = self.product_ids.filtered(lambda r: r.product_id == self.product_selection)
        if self.product_selection.id == False:
            raise ValidationError('Please select a product before trying to add product')
        if line:
            line.update({'quantity': self.product_quantity})
        else:
            product_manufactured = self.env['product.manufactured'].create({
                'product_id': self.product_selection.id,
                'quantity': self.product_quantity
            })
            self.update({
                'product_ids': [(4, product_manufactured.id)]
            })

        self.product_selection = False
        self.product_quantity = False

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.wizard',
            'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_view_form').id, 'form']],
            'target': 'new',
            'res_id': self.id,
        }

    def turnProcessedIntoProducts(self, lost_surface = 0):
        total_surface_used = 0

        if not self.product_ids:
            raise ValidationError("You have not selected any product, please do it")
        
        for product in self.product_ids:
            if product.quantity == 0:
                self.update({
                    'product_ids': [(2, product.id)]
                })    

        picking_type = self.env['stock.picking.type'].search([('name', '=', 'Manufacturing')], limit=1)
        surface_produced = 0

        for move in self.processed_mo.move_raw_ids:
            total_surface_used = total_surface_used + round(move.product_uom_qty * move.product_id.product_surface, 2)

        for product_manufactured in self.product_ids:
            surface_produced += round(product_manufactured.product_id.product_surface * product_manufactured.quantity,
                                      2)

        # if surface_produced + lost_surface < (total_surface_used - (
        #         total_surface_used * self.processed_wo.workcenter_id.error_margin)) or surface_produced > (
        #         total_surface_used + (total_surface_used * self.processed_wo.workcenter_id.error_margin)):
        #     missing_surface = total_surface_used - surface_produced
        #     msg = "The quantity produced is incorrect. \n Expected : %s \n Produced : %s \n Needed left : %s" % \
        #           (round(total_surface_used,2), round(surface_produced,2), round(missing_surface,2))
        #     context = {
        #         'default_text': msg,
        #         'default_error_amount': missing_surface,
        #         'default_wizard_id': self.id,
        #     }
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'popup.error',
        #         'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_error_form').id, 'form']],
        #         'context': context,
        #         'target': 'new',
        #     }

        for product_manufactured in self.product_ids:
            # Create a manufacturing order
            manuf_order = self.env['mrp.production'].create({
                'company_id': self.processed_mo.company_id.id,
                'consumption': 'flexible',
                'date_planned_start': self.processed_mo.date_planned_start,
                'location_dest_id': self.processed_mo.location_dest_id.id,
                'location_src_id': self.processed_mo.location_src_id.id,
                'picking_type_id': self.processed_mo.picking_type_id.id,
                'product_id': product_manufactured.product_id.id,
                'product_qty': product_manufactured.quantity,
                'qty_producing': product_manufactured.quantity,
                'product_uom_id': product_manufactured.product_id.uom_id.id,
                'original_mo': self.processed_mo.id,
            })
            # Create 2 Stock Moves,
            # 1 move for Consumable FROM WH/Stock TO Virtual/Production
            # 1 move for finished good FROM Virtual/Prod TO WH/Stock

            warehouse_location = self.env['stock.location'].search([('name', '=', 'Stock'), ('company_id', '=', self.env.company.id)], limit=1)
            production_location = self.env['stock.location'].search(
                [('name', '=', 'Production'), ('company_id', '=', self.env.company.id)], limit=1)
            name = manuf_order.name
            processed_product = self.env['product.product'].search([('name', '=', 'Process foot²')], limit=1)

            stock_move_processed_product = self.env['stock.move'].create({
                'company_id': self.processed_mo.company_id.id,
                'date': self.processed_mo.date_planned_start,
                'location_dest_id': production_location.id,
                'location_id': warehouse_location.id,
                'name': name,
                'procure_method': 'make_to_stock',
                'product_id': processed_product.id,
                'product_uom': processed_product.uom_id.id,
#                 'product_uom_qty': product_manufactured.quantity + lost_surface,
#                 'quantity_done': product_manufactured.quantity + lost_surface,
                'product_uom_qty': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
                'quantity_done': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
                'raw_material_production_id': manuf_order.id,
                'origin': manuf_order.name,
            })
            stock_move_final_product = self.env['stock.move'].create({
                'company_id': self.processed_mo.company_id.id,
                'date': self.processed_mo.date_planned_start,
                'location_dest_id': warehouse_location.id,
                'location_id': production_location.id,
                'name': name,
                'procure_method': 'make_to_stock',
                'product_id': product_manufactured.product_id.id,
                'product_uom': product_manufactured.product_id.uom_id.id,
                'production_id': manuf_order.id,
                # 'product_uom_qty': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
                # 'quantity_done': round(product_manufactured.quantity*product_manufactured.product_id.product_surface*processed_product.product_surface,2),
                'product_uom_qty': product_manufactured.quantity,
                'quantity_done': product_manufactured.quantity,
                'picking_type_id': picking_type.id,
                'origin': manuf_order.name,
                'reference':'Final stock move',
            })
  
            manuf_order.action_confirm()
            manuf_order.button_mark_done()

        action = self.processed_wo.with_context(no_start_next=True).do_finish()

        try:
            with self.processed_wo.env.cr.savepoint():
                res = self.processed_mo.button_mark_done()
                if res is not True:
                    res['context'] = dict(res['context'], from_workorder=True)
                    return res
        except (UserError, ValidationError) as e:
            # log next activity on MO with error message
            self.processed_mo.activity_schedule(
                'mail.mail_activity_data_warning',
                note=e.name,
                summary=('The %s could not be closed') % (self.processed_mo.name),
                user_id=self.env.user.id)

        return action


class PopupError(models.Model):
    _name = 'popup.error'

    wizard_id = fields.Many2one('mrp.wizard', string="Wizard ID")
    text = fields.Char(string="Error :", readonly=1)
    error_amount = fields.Float(string="Error amount")

    def addScrap(self):
        warehouse_location = self.env['stock.location'].search([('name', '=', 'Stock'), ('company_id', '=', self.env.company.id)], limit=1)
        production_location = self.env['stock.location'].search([('name', '=', 'Production'), ('company_id', '=', self.env.company.id)], limit=1)
        processed_product = self.env['product.product'].search([('name', '=', 'Process foot²')], limit=1)

        scrap = self.env['stock.scrap'].create({
                    'company_id': self.wizard_id.processed_mo.company_id.id,
                    'date_done': self.wizard_id.processed_mo.date_planned_start,
                    'scrap_location_id': warehouse_location.id,
                    'location_id': production_location.id,
                    # 'name': name,
                    'product_id': self.wizard_id.product_manufactured.product_id.id,
                    'product_uom_id': self.wizard_id.product_manufactured.product_id.uom_id.id,
                    # 'production_id': manuf_order.id,
                    'scrap_qty': lost_surface,
                    # 'picking_type_id': picking_type.id,
                    # 'origin': manuf_order.name,
                    # 'reference':'Final stock move',
                })
        return self.wizard_id.turnProcessedIntoProducts(self.error_amount)

    def goBack(self):
#         return {
#             'type': 'ir.actions.act_window_close'
#         }
        
        self.wizard_id._compute_bom_outcome(False)
            
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.wizard',
                'view_mode': 'form',
                'views': [[self.env.ref('cap_manufacturing_popup.wizard_popup_view_form').id, 'form']],
                'target': 'new',
                'res_id': self.wizard_id.id,
            }

    wizard_id = fields.Many2one('mrp.wizard', string="Wizard ID")
    text = fields.Char(string="Error :", readonly=1)
    error_amount = fields.Float(string="Error amount")

#Overriding the error message to allow use of the custom BOMs
#TODO : find why it's happening, it used to work flawlessly

class StockMove(models.Model):
    _inherit = "stock.move"


    def _set_product_qty(self):
        """ The meaning of product_qty field changed lately and is now a functional field computing the quantity
        in the default product UoM. This code has been added to raise an error if a write is made given a value
        for `product_qty`, where the same write should set the `product_uom_qty` field instead, in order to
        detect errors. """
        #raise UserError(_('The requested operation cannot be processed because of a programming error setting the `product_qty` field instead of the `product_uom_qty`.'))

        return True
