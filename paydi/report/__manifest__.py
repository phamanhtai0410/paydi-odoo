# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Report',
    'version': '0.1',
    'category': 'Productivity',
    'sequence': -100,
    'description': """Report: Listing""",
    'summary': 'Report: Listing',
    'depends': ['base', 'mail'],
    'license': 'LGPL-3',
    'data': [
        'views/report_transactions_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True
}

