
import json
import hashlib
import hmac
import os
from pkgutil import get_data
import requests
from odoo import fields, models, api, tools

def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()
class PosFunctions(models.Model):
    _name = 'pos.functions'
    _description = 'Description'

    feature = fields.Selection(string='Tính năng', selection=[('pre_auth', 'Pre Auth'), ('tip', 'TIP'), ('moto', 'Moto'), ('installment', 'Trả góp'), ('PNPL', 'Pay Now Pay Later')], default='pre_auth')
    disable = fields.Boolean(string='Khóa', default=True)
    pos_account_id = fields.Many2one('account.pos.machines', string='Tài khoản', readonly=True, auto_join=True)
    pos_bank = fields.One2many('pre.auth', string='pos_bank', inverse_name='pos_func')
    partner_id = fields.Many2one('res.partner')
    
    def detail_bank(self):       
        view_id = self.env.ref('pos_machines.pre_auth_form_view').id
        _pos_id = self.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Details',
            'res_model': 'pre.auth',
            'views': [(view_id, 'tree')],
            'target': 'new',
            'domain':[('feature','=', self.feature),('pos_func','=',_pos_id)],
            'context': 
                {
                    'default_feature': self.feature,
                    'default_pos_func': self.id,
                    'default_pos_id': self.pos_account_id.id
                }
        }
    
    def get_data(self):
        data = []
        self.env.cr.execute(""" SELECT  pos_functions.pos_account_id, pos_functions.feature, pos_functions.disable
                                FROM pos_functions
                                WHERE pos_functions.pos_account_id = %d"""%(self.pos_account_id.id))                   
        query=self.env.cr.dictfetchall()

        for x in query:
            data.append({
                'feature':x['feature'],
                'disable':x['disable']
            })
         
        self.env.cr.execute(""" SELECT pos_functions.feature, pre_auth.bank_id, pre_auth.is_blocked, res_bank.code 
                                FROM (( pre_auth
                                INNER JOIN pos_functions ON pos_functions.pos_account_id = pre_auth.pos_id AND pos_functions.feature = pre_auth.feature)
                                INNER JOIN res_bank ON pre_auth.bank_id = res_bank.id)
                                WHERE pos_functions.pos_account_id = %d
                                """%(self.pos_account_id.id))
        query2=self.env.cr.dictfetchall()
        
        pre_auth = []
        moto = []
        for x in query2:
            if(x['feature']=='pre_auth'):
                pre_auth.append({
                    'bank_id':x['bank_id'],
                    'is_blocked':x['is_blocked'],
                    'code':x['code']
                })
            else:
                moto.append({
                    'bank_id':x['bank_id'],
                    'is_blocked':x['is_blocked'],
                    'code':x['code']
                })
        for x in data:
            if(x['feature']=='pre_auth' and x['disable']==False):
                x.update({
                    'blocked_bank':pre_auth
                })
            elif(x['feature']=='moto' and x['disable']==False):
                x.update({
                    'blocked_bank':moto
                })
        
        self.ensure_one()
        secret_key = tools.config['mms_secret_key']  # 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        api_domain = tools.config['api_domain']
        api_key = tools.config['mms_api_key']
        
        # SECRET_KEY = os.getenv('SECRET_KEY')
        # URL_LOCAL = os.getenv('URL_LOCAL')
        # API_KEY = os.getenv('API_KEY')
        
        supporter_id = self.partner_id.supporter_id
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
        company_code = self.partner_id.parent_id.company_id.company_code if self.partner_id.parent_id else self.partner_id.company_id.company_code
        
        value = {
            "serial_number": str(self.pos_account_id.lot_id.name),
            "ref_codes": [x.ref_no for x in self.pos_account_id.ref_codes],
            "disable_functions": data,
            "odoo_contact_id": str(self.partner_id.id),
            "username": str(self.pos_account_id.username),
            'password': '000000',
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
                },
                'company_code': company_code or 'paydi'
            },
            'contact_seller': contact_seller,
        }
    
        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{api_domain}/v1/auth/iapi/pos/gen_account?api_key={api_key}"

        payload = json.dumps({
            **value,
            "code": hash_string,
        })
        print('``````` payload', payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        if not response.status_code == 200:
            raise Exception
        return 

    
    
    @api.model
    def write(self,values):
        super(PosFunctions, self).write(values)
        self.get_data()
        return True


   