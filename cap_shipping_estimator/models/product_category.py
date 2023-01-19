# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    delivery_carrier_ids = fields.Many2many("delivery.carrier", "product_cat_delivery_carrier_rel",
                                            "cat_id", "delivery_carrier_id", "Delivery Carrier")
