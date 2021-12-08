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
        'views/report_view.xml',
        'security/ir.model.access.csv',
        'views/list_transactions.xml',
        'views/report_template.xml',
        'views/list_customer_reports.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True
}

