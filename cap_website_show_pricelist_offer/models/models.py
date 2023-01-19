# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Website(models.Model):
    _inherit = 'website'

    @api.model
    def get_pricelist_details(self, curr_pl, product_template_id):
        res = super(Website, self).get_pricelist_details(curr_pl, product_template_id)
        res = res[::-1]
        return res
