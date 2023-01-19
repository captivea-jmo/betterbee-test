# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    height = fields.Float(string='Height')
    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
