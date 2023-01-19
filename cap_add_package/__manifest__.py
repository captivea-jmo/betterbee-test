# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Cap Add Delivery Packages',
    'version': '1.1',
    'category': 'Inventory/Delivery',
    'description': """
Allows you to add Multiple delivery packages on the Stock picking (Transfers).
==============================================================
This module is used to Allows you to add Multiple delivery packages on the 
Stock picking using Wizard.
""",
    'depends': ['stock'],
    'data': [
        "security/ir.model.access.csv",
        'wizard/product_pack_wiz.xml',
        'views/product_packaging_view.xml',

    ],
    'installable': True,
}
