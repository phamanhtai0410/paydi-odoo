import hashlib
import hmac
import json

import requests

from odoo import fields, models, api


def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()


class PosMachineSetting(models.Model):
    _name = 'pos.machine.setting'
    _description = 'Description'

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', readonly=True)
    stock_move_line = fields.Many2one('stock.move.line')
    partner = fields.Many2one('res.partner',
                              readonly=True,
                              string="Merchant")

    tid = fields.Char(string="Mã TID")

    mid = fields.Char(string="Mã MID")

    account = fields.Many2one('account.pos.machines',
                              string="Tài khoản PAYDI",
                              readonly=True)

    @api.model
    def create(self, vals):
        # if isinstance(vals, int):
        #     return super().write(vals)
        default = self.default_get(['lot_id', 'partner', 'stock_move_line'])
        print('[debug] create', vals, default)
        lot = self.env['stock.production.lot'].search_read([('id', '=', default.get('lot_id'))])
        if lot:
            lot = lot[0]
        partner = self.env['res.partner'].search_read([('id', '=', default.get('partner'))])
        if partner:
            partner = partner[0]
        secret_key = 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        value = {
            "serial_number": lot.get('name'),
            "tid": vals.get('tid'),
            "mid": vals.get('mid'),
            "odoo_contact_id": str(default.get('partner')),
            "username": f"{default.get('partner')}-{vals.get('tid')}",
            "pos_address": {
                "city": "TP.Hồ Chí Minh",
                "district": "TP.Thủ Đức",
                "ward": "TML",
                "detail": "11 Đường 32"
            },
            "merchant": {
                "name": partner.get('name'),
                "address": {
                    "city": "TP.Hồ Chí Minh",
                    "district": "TP.Thủ Đức",
                    "ward": "TML",
                    "detail": "11 Đường 32"
                }
            }
        }
        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = "https://paydi-staging.rinznetwork.com/v1/auth/iapi/pos/gen_account?api_key=api_key_12563698"

        payload = json.dumps({
            **value,
            "code": hash_string
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        if not response.status_code == 200:
            raise Exception

        ac = self.env['account.pos.machines'].create({
            'username': value.get('username'),
            'partner_id': default.get('partner'),
            'lot_id': default.get('lot_id'),
            'stock_move_line': default.get('stock_move_line')
        })
        ac.stock_move_line.write({
            'account': ac.id
        })
        vals['account'] = ac.id

        return super().create(vals)
