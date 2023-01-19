# -*- coding: utf-8 -*-
{
    'name': 'Late payment fee',
    'version': '0.1',
    'category': 'account_accountant',
    'summary': 'Adding a fee to the late payments',
    'depends': ['account_accountant','contacts'],
    'data': [
        'data/fee.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True

}
