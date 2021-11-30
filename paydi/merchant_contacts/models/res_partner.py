# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_vn_name = fields.Char(string='Tên đăng ký(VN)')
    company_en_name = fields.Char(string='Tên đăng ký(EN)')

    obj_type = fields.Selection(selection='get_obj_type_options', string="Loại liên hệ")

    @api.model
    def get_obj_type_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'obj_type'), ('model', '=', 'res.partner')])
        return [(x.get('value'), x.get('name')) for x in options]

    business_type = fields.Selection(selection='get_business_type_options', string='Loại hình công ty')

    @api.model
    def get_business_type_options(self):
        options = self.env['master.data'].search_read(
            [('field', '=', 'business_type'), ('model', '=', 'res.partner')])
        return [(x.get('value'), x.get('name')) for x in options]

    registration_number = fields.Char(string="Số đăng ký kinh doanh")

    service_ids = fields.One2many('merchant.service', 'partner_id', string="Dịch vụ khác")
