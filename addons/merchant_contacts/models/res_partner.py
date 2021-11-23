# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    obj_type = fields.Selection([
        ('', ''),
        ('merchant', 'Đối tác máy Pos'),
    ], string="merchant")
