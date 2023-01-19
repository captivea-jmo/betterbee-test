# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_enable_gdpr = fields.Boolean(
        "Enable GDPR",
        related="website_id.is_enable_gdpr", readonly=False)
    is_enable_email = fields.Boolean(
        "Enable Responsible Person Email Notification",
        related="website_id.is_enable_email", readonly=False)
    user_ids = fields.Many2many(
        "res.users", string="Responsible Person",
        related="website_id.user_ids", readonly=False)
    is_customer = fields.Boolean(
        "Enable Customer Email Notification",
        related="website_id.is_customer", readonly=False)
