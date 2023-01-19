# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.exceptions import UserError


class WebsiteSaleDelivery(WebsiteSaleDelivery):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        print("\n\npost---custom-->", post)
        order = request.website.sale_get_order()
        carrier_id = post.get('carrier_id')
        if carrier_id:
            carrier_id = int(carrier_id)
        if order:
            order.with_context({'rate': 1})._check_carrier_quotation(force_carrier_id=carrier_id)
            if carrier_id:
                return request.redirect("/shop/payment")

        return super(WebsiteSaleDelivery, self).payment(**post)
