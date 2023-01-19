# coding: utf-8

{
    'name': "Cap Shipping estimator",
    'author': 'Captivea',
    'website': 'www.captivea.us',
    'version': '1.0.0',
    'category': 'sale',
    'summary': """Change get all delivery carrier with its estimation cost on selection of delivery carrier.""",
    'license': 'AGPL-3',
    'description': """Change get all delivery carrier with its estimation cost on selection of delivery carrier.""",
    'depends': ['delivery', 'easypost_delivery', 'product', 'website_sale_delivery'],
    'data': [
        'views/product_category_view.xml',
        'views/stock_quant_package.xml',
        'views/stock_picking_views.xml',
        'wizard/choose_delivery_carrier_views.xml',
        'wizard/choose_delivery_package_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
