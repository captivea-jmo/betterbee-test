# -*- coding: utf-8 -*-
{
    'name': "Website Show Pricelist Offers",

    'summary': """Show Bulk Quantity Offers in Website""",

    'description': """This module will help you to show the pricelist offers for produces with different quantities. 
    This will increase the overall sale""",

    'author': 'ErpMstar Solutions',
    'category': 'Website',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.jpg'],
    'live_test_url': 'https://youtu.be/NBzjzdXcCjI',
    'website': '',
    'auto_install': False,
    'price': 50,
    'currency': 'EUR',
}
