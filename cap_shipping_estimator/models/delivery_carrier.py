# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_cost = fields.Float(string='Delivery Cost')

    def button_confirm(self):
        wizard = self.env['choose.delivery.carrier'].browse(self.env.context.get('wizard_id'))
        wizard.write({'carrier_id': self.id, 'delivery_price': self.delivery_cost})
        wizard.button_confirm()