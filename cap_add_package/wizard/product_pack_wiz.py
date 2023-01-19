# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductPackagingWizard(models.TransientModel):
    _name = 'product.package.wiz'

    @api.model
    def default_get(self, fields):
        rec = super(ProductPackagingWizard, self).default_get(fields)
        picking_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        rec.update({"picking_id": picking_id.id})
        return rec

    product_packaging_ids = fields.Many2many('product.packaging', string='Product Packaging')
    picking_id = fields.Many2one("stock.picking", "Picking")

    def add_product_packaging(self):
        recs = self.env['x_packed_boxes']
        for line in self.product_packaging_ids:
            for i in range(0, line.number):
                recs |= self.env['x_packed_boxes'].create({
                    'x_studio_transfer': self.picking_id.id,
                    'x_studio_box_type': line.id,
                    'x_studio_packed_weight': line.max_weight,
                    'x_studio_packed_height': line.height,
                    'x_studio_packed_length': line.packaging_length,
                    'x_studio_packed_width': line.width,
                    # 'x_studio_packed_number': line.number,
                })
            line.write({'number': 1})
        self.picking_id.write({'x_studio_packed_boxes': [(4, rec.id) for rec in recs]})
