# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mid management',
    'category': 'Sales/CRM',
    'sequence': -10,
    'summary': 'Mid management center',
    'description': """Mid management center""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'view/mid.xml',
        'view/assets.xml',
        'view/add-mid-template.xml',
        'view/list-mid-template.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
}