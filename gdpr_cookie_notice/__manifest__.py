# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
{
    'name': 'Cookie Consent Manager / GDPR / EU',
    'description': """
        - Cookie management for Google Analytics, Live Chat, Essential, Advertising, & Much more.
        - GDPR Cookie Law
        - 100% EU GDPR Cookie compliance Odoo
        - All in one cookie management
        - Predefined Themes for cookie popup
        - Different positions for cookie popup
        - Responsive & Mobile Friendly
        - Cross Browser Support
        - Light Weight
        - Fully Customizable 
    """,
    'summary': 'Fully Customizable Website Cookie Manager in Odoo',
    'category': 'Website',
    'version': '14.0.1.1.1',
    'author': 'TechKhedut Inc.',
    'company': 'TechKhedut Inc.',
    'maintainer': 'TechKhedut Inc.',
    'website': "https://www.techkhedut.com",
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/data.xml',
        'views/website_cookie_notice_views.xml',
        'views/assets.xml',
    ],
    'images': ['static/description/eu-gdpr-website-cookie-notice-odoo.gif'],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 66.4,
    'currency': 'EUR',
}
