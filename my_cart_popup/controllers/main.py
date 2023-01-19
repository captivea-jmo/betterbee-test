# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.
from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.misc import get_lang

global_no_varient_attr = []
global_custom_attr = []


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/cart/update_json_popup'], type='json', auth="public", methods=['POST'], website=True,
                csrf=False)
    def cart_update_json_popup(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
                               no_varient=None, custom_attribute=None):
        global global_no_varient_attr
        global global_custom_attr
        global_no_varient_attr = no_varient
        global_custom_attr = custom_attribute
        return_vals = self.cart_update_json(product_id, line_id, add_qty, set_qty, display)
        return return_vals

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        no_variant_attribute_values = global_no_varient_attr if global_no_varient_attr else []
        product_custom_attribute_values = global_custom_attr if global_custom_attr else []
        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty,
                                   no_variant_attribute_values=no_variant_attribute_values,
                                   product_custom_attribute_values=product_custom_attribute_values)

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        lang = get_lang(request.env).code

        value['website_sale.cart_lines'] = request.env['ir.ui.view'].with_context(lang=lang)._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template(
            "website_sale.short_cart_summary", {
                'website_sale_order': order,
            })

        return value
