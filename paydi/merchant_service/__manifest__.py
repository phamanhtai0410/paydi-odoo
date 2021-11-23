# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Merchant service',
    'category': 'Sales',
    'summary': 'List service for merchant',
    'depends': [],
    'data': [
        'views/merchant_service.xml',
        'security/ir.model.access.csv'
    ],
    'application': True
}
