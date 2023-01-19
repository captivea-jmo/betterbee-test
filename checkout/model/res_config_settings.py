from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    checkout_promo_text = fields.Char(string='Text fro Promos/Discounts', config_parameter='checkout.checkout_promo_text')