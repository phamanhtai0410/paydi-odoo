from email.policy import default
import json
import hashlib
import hmac
import os
import requests
from odoo import fields, models, api, tools
from . import pos_functions

class PreAuthentication(models.Model):
    _name = 'pre.auth'
    _description = 'Description'
    
    bank_id = fields.Many2one('res.bank', string='Ngân hàng')
    
    pos_account_id = fields.Many2one('pos.functions', string='pos_account_id',inverse_name='pos_account_id')
    is_blocked = fields.Boolean(default=False, string='Khóa')
    feature = fields.Char()
    
    # @api.model
    # def write(self,values):
    #     super(PreAuthentication, self).write(values)
    #     aaa = []
    #     lis_val = self.pos_account_id.feature
    #     # pos_functions.PosFunctions.write(aaa)
    #     # self.pool.get('pos.functions').write(values)
        
    #     return self.env["pos.functions"].write(aaa)
    