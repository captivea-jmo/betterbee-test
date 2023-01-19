from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        warning = super(SaleOrderLine, self)._onchange_product_uom_qty()
        error = False
        throw_error = self.product_template_id.x_studio_throw_error
        current_product = self.product_template_id
        bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', current_product.id)], limit=1)

        result = self.getErrorInQuantity(error, bom, self.product_uom_qty)

        if throw_error and result:
            text = 'Component doesn\'t have the required quantity to be manufactured. \nProduct : ' + str(
                bom.product_tmpl_id.name)
            warning_mess = {
                'title': _('Warning'),
                'message': _(text),
            }
            return {'warning': warning_mess}
        else:
            return warning

    def getErrorInQuantity(self, error, bom, qty):
        for bom_line in bom.bom_line_ids:
            if bom_line.product_id.qty_available < bom_line.product_qty * qty:
                error = True
            elif bom_line.product_id.bom_count > 0:
                bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', bom_line.product_id.id)], limit=1)
                self.getErrorInQuantity(error, bom, qty)

        return error
