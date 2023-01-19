from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    days_for_fee = fields.Integer(string="Late fee days",help="Number of days before triggering the Late fee", default="30")
    late_fee_boolean = fields.Boolean(string="Late fee if late payment", default=True)
    late_fee_price = fields.Float(string="Fee amount",default=0.1)
