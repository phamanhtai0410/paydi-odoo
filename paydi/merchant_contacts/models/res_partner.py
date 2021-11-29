# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_vn_name = fields.Char(string='Tên đăng ký(VN)')
    company_en_name = fields.Char(string='Tên đăng ký(EN)')

    obj_type = fields.Selection([
        ('merchant', 'Đối tác máy Pos'),
    ], string="Loại liên hệ")

    business_type = fields.Selection([
        ('C_TNHH', 'Công ty TNHH'),
        ('C_CP', 'Công ty Cổ phần'),
    ], string='Loại hình công ty')

    registration_number = fields.Char(string="Số đăng ký kinh doanh")

    service_ids = fields.One2many('m.service', 'partner_id', string="Dịch vụ khác")

    mid = fields.One2many('mms.mid', 'partner_id',  string='Mã mid')
