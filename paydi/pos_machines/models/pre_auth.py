from email.policy import default
import json
import hashlib
import hmac
import os
import re
from xmlrpc.client import boolean
import requests
from odoo import fields, models, api, tools
from . import pos_functions

def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()
class PreAuthentication(models.Model):
    _name = 'pre.auth'
    _description = 'Description'
    
    bank_id = fields.Many2one('res.bank', string='Ngân hàng', domain="[('code', '!=', False)]")
    pos_func = fields.Many2one('pos.functions', string='pos_func')
    is_blocked = fields.Boolean(default=False, string='Khóa')
    feature = fields.Char()
    pos_id = fields.Integer()

    @api.model
    def create(self,values):
        result = super(PreAuthentication, self).create(values)
        print("het",self.env['pos.functions'].search([('id', '=', values.get('pos_func'))]).get_data())
        return result

    def write(self,values):
        result = super(PreAuthentication, self).write(values)
        self.env['pos.functions'].search([('id', '=', self.pos_func.id)]).get_data()
        return result