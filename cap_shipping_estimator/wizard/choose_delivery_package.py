# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.tools.float_utils import float_compare


class ChooseDeliveryPackage(models.TransientModel):
    _inherit = 'choose.delivery.package'

    def _get_default_length_uom(self):
        return self.env['product.template']._get_length_uom_name_from_ir_config_parameter()

    height = fields.Float(string='Height')
    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
    is_custom_parcel = fields.Char(string='Custom Parcel', related='delivery_packaging_id.shipper_package_code')
    length_uom_name = fields.Char(string='Length unit of measure label', compute='_compute_length_uom_name', default=_get_default_length_uom)

    def _compute_length_uom_name(self):
        for packaging in self:
            packaging.length_uom_name = self.env['product.template']._get_length_uom_name_from_ir_config_parameter()

    @api.onchange('delivery_packaging_id')
    def _on_change_delivery_package_id(self):
        """ Height, Width and Length will be set on when we have Custom Parcel
            we are Populate the Values from the Custom Parcel vales and set it on change
        """
        if self.delivery_packaging_id:
            self.height = self.delivery_packaging_id.height
            self.width = self.delivery_packaging_id.width
            self.length = self.delivery_packaging_id.packaging_length

    # overwrite want record in stock_quant_package height,width,length
    def action_put_in_pack(self):
        picking_move_lines = self.picking_id.move_line_ids
        if not self.picking_id.picking_type_id.show_reserved and not self.env.context.get('barcode_view'):
            picking_move_lines = self.picking_id.move_line_nosuggest_ids

        move_line_ids = picking_move_lines.filtered(lambda ml:
                                                    float_compare(ml.qty_done, 0.0,
                                                                  precision_rounding=ml.product_uom_id.rounding) > 0
                                                    and not ml.result_package_id
                                                    )
        if not move_line_ids:
            move_line_ids = picking_move_lines.filtered(lambda ml: float_compare(ml.product_uom_qty, 0.0,
                                                                                 precision_rounding=ml.product_uom_id.rounding) > 0 and float_compare(
                ml.qty_done, 0.0,
                precision_rounding=ml.product_uom_id.rounding) == 0)

        delivery_package = self.picking_id._put_in_pack(move_line_ids)
        # write shipping weight and product_packaging on 'stock_quant_package' if needed
        if self.delivery_packaging_id:
            delivery_package.packaging_id = self.delivery_packaging_id
        if self.shipping_weight:
            delivery_package.shipping_weight = self.shipping_weight
        # for custom parcel height, width and length
        if self.height:
            delivery_package.height = self.height
        if self.width:
            delivery_package.width = self.width
        if self.length:
            delivery_package.length = self.length
