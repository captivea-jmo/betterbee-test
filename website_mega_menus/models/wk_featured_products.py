# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class WkCarousel(models.Model):
    _name = "wk.mega.menu.featured.products"

    name = fields.Char('Name')
    product_ids = fields.Many2many(
    'product.template',
    string="Products",
    required=True)

    def unlink(self):
        mega_menu = self.env['website.menu'].search([('featured_products_id','in',self.ids)])
        if mega_menu:
            raise ValidationError("This record is being used by a menu item")
        else:
            return super(WkCarousel, self).unlink()
