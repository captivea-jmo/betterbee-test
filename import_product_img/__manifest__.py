{
    'name': 'Import Product Images',
    'version': '14.0',
    'sequence': 1,
    'category': 'Extra Tools',
    'summary': 'import images',
    'description': """
    Import Images
    """,
    'depends': ['base', 'sale',
                'account',
                'sale_management'],
    'data': [
            'security/ir.model.access.csv',
            'wizard/product_view.xml',
             ],
    'installable': True,
    'auto_install': False,
}
