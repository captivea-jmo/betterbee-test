# -*- coding: utf-8 -*-

{
    # Module Information
    'name': 'Ajax cart | Quantity option in Website(Webshop)',
    'category': 'Website/eCommerce',
    'summary': 'Add product to cart without refresh the page with the quantity option, quick add cart, Add cart using Ajax',
    'version': '14.0.0.1',
    "description": """
        Add product to cart with quantity,
        select quantity in shop,
        Add product to cart without refresh the page, 
        quick add cart, 
        add to cart using ajax,
        product add to cart quickly,
        Ajax Add to Cart,
        Add cart using Ajax,
        cart ajax, add product, add to cart ajax,
        ajax add to cart,
        ajax cart,
        add to cart,
        cart,
        ajax,
        
    """,
    'license': 'OPL-1',    
    'depends': ['website_sale'],

    'data': [
        'views/res_config_settings_views.xml',
        'templates/assets.xml',
        'templates/website_sale_templates.xml',
    ],

    #Odoo Store Specific
    'images': [
        'static/description/ajax_cart.png',
    ],

    # Author
    'author': 'AV Technolabs',
    'website': 'http://avtechnolabs.com',
    'maintainer': 'AV Technolabs',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 22,
    "live_test_url":'https://youtu.be/lsvr-0tgrmc',
    'currency': 'EUR', 
}
