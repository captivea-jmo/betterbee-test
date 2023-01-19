# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    is_enable_gdpr = fields.Boolean("Enable GDPR")
    is_enable_email = fields.Boolean("Responsible Person")
    user_ids = fields.Many2many("res.users", string="User")
    is_customer = fields.Boolean("Customer")
