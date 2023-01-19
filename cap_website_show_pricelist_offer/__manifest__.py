# -*- coding: utf-8 -*-
{
    'name': "CAP Custom website_show_pricelist_offer",

    'summary': """
        Customization BetterBee/Humble Abodes for website_show_pricelist_offer""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Thomas Petithory @ Captivea",
    'website': "https://www.captivea.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'website_show_pricelist_offer',
    ],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
