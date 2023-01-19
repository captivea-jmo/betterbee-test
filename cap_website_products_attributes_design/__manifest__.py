{
    'name': 'Cap website products attributes selection',
    'version': '1.0',
    'category': 'website',
    'sequence': 240,
    'summary': 'This module used for change a attributes selection on website.',
    'description': """
This module used for change a attributes selection on website.
==================================================
Attributes selection on different types on website products.
       """,
    'website': 'https://www.captivea.com',
    'depends': ['website_sale'],
    'data': [
        'views/templates.xml',
        'views/product_template_view.xml',
        'views/product_attribute_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
