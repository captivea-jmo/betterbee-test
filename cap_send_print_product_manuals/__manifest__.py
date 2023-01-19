# -*- coding: utf-8 -*-
{
    'name': 'Send and print product manuals module',
    'version': '0.2',
    'category': 'account_accountant',
    'summary': 'Allows to print manuals from Invoice, and to send manuals from invoice',
    'depends': ['account_accountant'],
    'data': [
        'views/print.xml',
        'views/email.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True

}
