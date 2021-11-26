# -*- coding: utf-8 -*-

# File: m_service.py	
# Created at 23/11/2021
from odoo import api, models, modules, fields


class MService(models.Model):
    _name = 'm.service'

    name = fields.Selection([
        ('dong_hanh', 'Đồng hành'),
        ('khuyen_mai', 'Khuyến mãi'),
        ('qua_sn', 'Quà sinh nhật'),
    ], string="Dịch vụ")
    has_used = fields.Boolean(string="Có dùng")
    note = fields.Char(string="Ghi chú")

    partner_id = fields.Many2one('res.partner', string='Hồ sơ')
