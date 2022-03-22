# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import hashlib
import hmac
import json

import requests

from odoo import api, models, tools, fields


def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()


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

    registration_number = fields.Char(string="Số đăng ký kinh doanh")

    # mid = fields.One2many('mms.mid', 'partner_id',  string='Mã mid'2)
    service_ids = fields.One2many('merchant.service', 'partner_id', string="Dịch vụ khác")

    def _get_city_code(self):
        for record in self:
            if record.city:
                record.city_code = self.env['vn.location'].search([('code', '=', record.city_code)], limit=1)

    def _set_city_code(self):
        for record in self:
            if record.city_code:
                record.city = record.city_code.code

    city_id = fields.Many2one('vn.location', string="Tỉnh/TP", domain=[('parent_id', '=', False)])

    district_id = fields.Many2one('vn.location', string="Quận/Huyện")

    ward_id = fields.Many2one('vn.location', string="Phường/xã")

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id and self.district_id and self.city_id.id != self.district_id.parent_id.id:
            self.district_id = None
            self.ward_id = None

    @api.onchange('district_id')
    def onchange_district_id(self):
        if self.district_id and self.ward_id and self.district_id.id != self.ward_id.parent_id.id:
            self.ward_id = None

    supporter_id = fields.Many2one('hr.employee',
                                   check_company=True,
                                   string="Nhân viên hỗ trợ"
                                   )
    supporter_department_id = fields.Many2one('hr.department',
                                              string="Đội ngũ hỗ trợ",
                                              related='supporter_id.department_id')

    @api.onchange('supporter_id')
    def onchange_supporter_id(self):
        print('___________________________________DEBUG___________________________________________')
        try:
            self.ensure_one()
            print("before", self.supporter_id)
            if self.supporter_id:
                secret_key = tools.config['mms_secret_key']  # 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
                api_domain = tools.config['api_domain']
                api_key = tools.config['mms_api_key']
                contact_seller = {
                    'phone': '',
                    'email': '',
                    'name': '',
                    'company': self.partner_id.company_id.name,
                    'mms_user_id': 0
                }
                if self.supporter_id:
                    contact_seller['phone'] = self.supporter_id.mobile_phone or ''
                    contact_seller['email'] = self.supporter_id.work_email or ''
                    contact_seller['name'] = self.supporter_id.name or ''
                    contact_seller['mms_user_id'] = self.supporter_id.id
                print('contact_seller', contact_seller)
                value = {
                    "contact_id": str(self.id),
                    'contact_seller': contact_seller
                }
                gen_data = sorted(value.items())
                string_data = json.dumps(gen_data)
                hash_string = sha512(string_data, secret_key)
                headers = {
                    'Content-Type': 'application/json'
                }
                url = f"{api_domain}/v1/auth/iapi/pos/info?api_key={api_key}"

                payload = json.dumps({
                    **value,
                    "code": hash_string
                })
                response = requests.request("PUT", url, headers=headers, data=payload)

                print(response.text)
        except Exception as e:
            print(e)
