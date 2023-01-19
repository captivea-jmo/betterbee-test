# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class ProductRibbon(models.Model):
    _inherit = "product.ribbon"

    html_class = fields.Char(string='Ribbon class', required=True, default='o_ribbon_left')

    sh_shop_product_sticker_product_sticker_style = fields.Selection([
        ('sh_shop_product_sticker_product_sticker_style_1','Style 1'),
        ('sh_shop_product_sticker_product_sticker_style_2','Style 2'),
        ('sh_shop_product_sticker_product_sticker_style_3','Style 3'),
        ('sh_shop_product_sticker_product_sticker_style_4','Style 4'),
        ('sh_shop_product_sticker_product_sticker_style_5','Style 5'),
        ('sh_shop_product_sticker_product_sticker_style_6','Style 6'),
        ('sh_shop_product_sticker_product_sticker_style_7','Style 7'),
        ('sh_shop_product_sticker_product_sticker_style_8','Style 8'),
        ('sh_shop_product_sticker_product_sticker_style_9','Style 9'),
        ('sh_shop_product_sticker_product_sticker_style_10','Style 10'),
        ('sh_shop_product_sticker_product_sticker_style_11','Style 11'),
        ('sh_shop_product_sticker_product_sticker_style_12','Style 12'),
        ('sh_shop_product_sticker_product_sticker_style_13','Style 13'),
        ('sh_shop_product_sticker_product_sticker_style_14','Style 14'),
        ('sh_shop_product_sticker_product_sticker_style_15','Style 15'),
        ],default='sh_shop_product_sticker_product_sticker_style_1',string='Ribbon Style')
    
    sh_shop_product_sticker_product_sticker_bg_color = fields.Char(
        string='Ribbon Background Color'
        )
    
    sh_shop_product_sticker_product_sticker_text_color = fields.Char(
        string='Ribbon Text Color'
        )