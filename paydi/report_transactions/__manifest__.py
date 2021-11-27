# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Transactions Report',
    'version': '0.1',
    'category': 'Productivity',
    'sequence': -100,
    'description': """Transactions Report: Listing""",
    'summary': 'Transactions Report: Listing',
    'depends': ['base', 'mail'],
    'license': 'LGPL-3',
    'data': [
        'views/report_transactions_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True
}

