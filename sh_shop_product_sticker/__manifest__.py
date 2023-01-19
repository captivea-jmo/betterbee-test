# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Website Product Sticker",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "license": "OPL-1",
    "summary": "Shop Product Sticker,Website Product Label,Product Custom Label,Product Custom Sticker,Product Label,website different sticker,website product Ribbon,e commerce product label,e commerce product sticker,shop product tag,website label,item Ribbon Odoo",
    "description": """This module allows you to set custom stickers for your items, which displays on the website as a ribbon. We provide unique 15 styles for ribbon. You can choose the ribbon background color, ribbon text color & ribbon style as per your product. You can attract customers using attractive stickers on products!""",
    "version": "14.0.1",
    "depends": [
        'website_sale',
    ],
    "application": True,
    "data": [
        "views/product_sticker_view.xml",
        "views/shop_templ.xml",
        "views/assets_frontend.xml",
    ], 
    "images": ["static/description/background.png", ], 
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": "EUR"
}
