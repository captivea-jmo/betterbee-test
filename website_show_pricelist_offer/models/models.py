# -*- coding: utf-8 -*-

from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def get_pricelist_details(self, curr_pl, product_template_id):
        item_ids = curr_pl.item_ids
        applied_rule = []
        for item_id in item_ids:
            applied_on = item_id.applied_on
            min_quantity = item_id.min_quantity
            if min_quantity > 1:
                if applied_on == '0_product_variant':
                    product_id = item_id.product_id
                    product_variant_ids = product_template_id.product_variant_ids

                    for product_variant_id in product_variant_ids:
                        if product_id == product_variant_id:
                            price = curr_pl.get_products_price([product_variant_id], [min_quantity],
                                                               [self.env.user.partner_id])
                            applied_rule.append({
                                "attribute_values": product_variant_id.product_template_attribute_value_ids.ids,
                                "product_tmpl_id": product_template_id.id,
                                "variant_id": product_variant_id.id,
                                "variant": product_variant_id.name_get()[0][1],
                                "qty": str(min_quantity),
                                "unit_price": price[product_variant_id.id],
                                "list_price": product_variant_id.lst_price
                            })
                elif applied_on == '1_product':
                    product_tmpl_id = item_id.product_tmpl_id
                    if product_template_id == product_tmpl_id:
                        product_variant_ids = product_template_id.product_variant_ids
                        if len(product_variant_ids) == 1:
                            price = curr_pl.get_products_price([product_variant_ids], [min_quantity],
                                                               [self.env.user.partner_id])
                            applied_rule.append({
                                'attribute_values': product_variant_ids.product_template_attribute_value_ids.ids,
                                "product_tmpl_id": product_template_id.id,
                                'variant_id': product_variant_ids.id,
                                'variant': product_variant_ids.name_get()[0][1],
                                'qty': str(min_quantity),
                                'unit_price': price[product_variant_ids.id],
                                'list_price': product_variant_ids.lst_price
                            })
                        if len(product_variant_ids) > 1:
                            for product_variant_id in product_variant_ids:
                                price = curr_pl.get_products_price([product_variant_id], [min_quantity],
                                                                   [self.env.user.partner_id])
                                applied_rule.append({
                                    'attribute_values': product_variant_id.product_template_attribute_value_ids.ids,
                                    "product_tmpl_id": product_template_id.id,
                                    'variant_id': product_variant_id.id,
                                    'variant': product_variant_id.name_get()[0][1],
                                    'qty': str(min_quantity),
                                    'unit_price': price[product_variant_id.id],
                                    'list_price': product_variant_id.lst_price
                                })
                elif applied_on == '2_product_category':
                    categ_id = item_id.categ_id
                    category_id = product_template_id.categ_id
                    if category_id == categ_id:
                        product_variant_ids = product_template_id.product_variant_ids
                        if len(product_variant_ids) == 1:
                            price = curr_pl.get_products_price([product_variant_ids], [min_quantity],
                                                               [self.env.user.partner_id])
                            applied_rule.append({
                                'attribute_values': product_variant_ids.product_template_attribute_value_ids.ids,
                                "product_tmpl_id": product_template_id.id,
                                'variant_id': product_variant_ids.id,
                                'variant': product_variant_ids.name_get()[0][1],
                                'qty': str(min_quantity),
                                'unit_price': price[product_variant_ids.id],
                                'list_price': product_variant_ids.lst_price
                            })
                        if len(product_variant_ids) > 1:
                            for product_variant_id in product_variant_ids:
                                price = curr_pl.get_products_price([product_variant_id], [min_quantity],
                                                                   [self.env.user.partner_id])
                                applied_rule.append({
                                    'attribute_values': product_variant_id.product_template_attribute_value_ids.ids,
                                    "product_tmpl_id": product_template_id.id,
                                    'variant_id': product_variant_id.id,
                                    'variant': product_variant_id.name_get()[0][1],
                                    'qty': str(min_quantity),
                                    'unit_price': price[product_variant_id.id],
                                    'list_price': product_variant_id.lst_price
                                })
                elif applied_on == '3_global':
                    product_variant_ids = product_template_id.product_variant_ids
                    if len(product_variant_ids) == 1:
                        price = curr_pl.get_products_price([product_variant_ids], [min_quantity],
                                                           [self.env.user.partner_id])
                        applied_rule.append({
                            'attribute_values': product_variant_ids.product_template_attribute_value_ids.ids,
                            "product_tmpl_id": product_template_id.id,
                            'variant_id': product_variant_ids.id,
                            'variant': product_variant_ids.name_get()[0][1],
                            'qty': str(min_quantity),
                            'unit_price': price[product_variant_ids.id],
                            'list_price': product_variant_ids.lst_price
                        })
                    if len(product_variant_ids) > 1:
                        for product_variant_id in product_variant_ids:
                            price = curr_pl.get_products_price([product_variant_id], [min_quantity],
                                                               [self.env.user.partner_id])
                            applied_rule.append({
                                'attribute_values': product_variant_id.product_template_attribute_value_ids.ids,
                                "product_tmpl_id": product_template_id.id,
                                'variant_id': product_variant_id.id,
                                'variant': product_variant_id.name_get()[0][1],
                                'qty': str(min_quantity),
                                'unit_price': price[product_variant_id.id],
                                'list_price': product_variant_id.lst_price
                            })
        print("rules", applied_rule)
        return applied_rule
