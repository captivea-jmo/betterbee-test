# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    select_carrier_ids = fields.Many2many("delivery.carrier", "choose_delivery_carrier_delivery_carrier_rel",
                                          "choose_delivery_wizard_id", "delivery_carrier_id", "Delivery Carrier")

