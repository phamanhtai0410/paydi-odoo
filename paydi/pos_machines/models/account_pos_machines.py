import hashlib
import hmac
import json

import requests

from odoo import fields, models, api, tools


def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()


class AccountPosMachines(models.Model):
    _name = 'account.pos.machines'
    _rec_name = 'username'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    _description = 'Pos machines'

    move_line_id = fields.Many2one(
        'stock.move.line')

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', readonly=True)

    username = fields.Char(
        string="Account",
        readonly=True
    )

    partner_id = fields.Many2one('res.partner', string="Merchant")

    states = fields.Selection(selection='get_states_options', string='Trạng thái máy', tracking=True)

    ref_code = fields.Char(string="Mã ref")

    disable_functions = fields.One2many('pos.functions', 'pos_account_id')

    @api.model
    def get_states_options(self):
        options = self.env['master.data'].search_read(
            [('field', '=', 'states'), ('model', '=', 'account.pos.machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    note = fields.Text(string='Ghi chú')

    def send_backend(self):
        self.ensure_one()
        secret_key = tools.config['mms_secret_key'] #'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        api_domain = tools.config['api_domain']
        api_key = tools.config['mms_api_key']
        supporter_id = self.supporter_id
        contact_seller = {
            'phone': '',
            'email': '',
            'name': '',
            'company': self.partner_id.company_id.name,
            'mms_user_id': 0
        }

        if supporter_id:
            contact_seller['phone'] = supporter_id.mobile_phone or ''
            contact_seller['email'] = supporter_id.work_email or ''
            contact_seller['name'] = supporter_id.name or ''
            contact_seller['mms_user_id'] = supporter_id.id

        value = {
            "serial_number": self.lot_id.name,
            "ref_code": self.ref_code,
            "disable_functions": [x.name for x in self.disable_functions],
            "odoo_contact_id": str(self.partner_id.id),
            "username": self.username,
            "pos_address": {
                "city": self.partner_id.state_id.name or '',
                "district": self.partner_id.city or '',
                "ward": self.partner_id.street2 or '',
                "detail": self.partner_id.street or ''
            },
            "merchant": {
                "name": self.partner_id.name,
                "address": {
                    "city": self.partner_id.state_id.name or '',
                    "district": self.partner_id.city or '',
                    "ward": self.partner_id.street2 or '',
                    "detail": self.partner_id.street or ''
                }
            },
            'contact_seller': contact_seller
        }
        # print('send_backend', value)

        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{api_domain}/v1/auth/iapi/pos/gen_account?api_key={api_key}"

        payload = json.dumps({
            **value,
            "code": hash_string
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        if not response.status_code == 200:
            raise Exception

        return True

    @api.model
    def create(self, vals):
        pos_account = super().create(vals)
        default_disable_functions = self.env['pos.functions'].create({
            'name': 'pre_auth',
            'disable': True,
            'pos_account_id': pos_account.id
        })

        return pos_account

    @api.model_create_multi
    def create(self, vals_list):
        print('[debug]  model_create_multi')
        for values in vals_list:
            print('model_create_multi', values)
        accounts = super(AccountPosMachines, self).create(vals_list=vals_list)
        default_disable_functions = self.env['pos.functions'].create([{
            'name': 'pre_auth',
            'disable': True,
            'pos_account_id': ac.id
        } for ac in accounts])
        print('default', default_disable_functions)
        return accounts
