# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing extended',
    'version': '0.1',
    'category': 'sales',
    'summary': 'manufacturing - popup - extended',
    'depends': ['sale_stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard.xml',
        'views/product_manufactured.xml',
        'views/mrp_production.xml',
        'views/mrp_workorder.xml'
        #'data/automations.py'
    
    ],
    'installable': True,
    'application': True

}
