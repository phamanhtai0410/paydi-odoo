import os
from odoo import fields, models, api
import requests
import datetime

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    odoo_contact_id = fields.One2many(comodel_name="fee.installment", string="odoo contact id",inverse_name="merchant_id")
    id_by_transaction = fields.One2many(comodel_name="transaction.installment", string="id_by_transaction", inverse_name="contact_id")

    def get_fee_installment(self, arg):
        _merchant_id = int(arg.get('odoo_contact_id'))
        fee_by_merchant = self.env["fee.installment"].sudo().search([("merchant_id","=",_merchant_id)])
        result = []
      
        for rec in fee_by_merchant:
            result.append({
                
                "name": rec['bank']['name'],
                "bank_code":rec['bank']['code'] if rec['bank']['code'] else '',
                "period" : rec['period'],
                "fee_installment" : rec['fee_installment'],
                "from_date" : rec['from_date'],
                "to_date" : rec['to_date']
            })
        return result

    
    def get_transaction_installment(self):
        _id = self.id
        transaction_late = self.env["transaction.installment"].search_read([("contact_id","=",_id)])

        if len(transaction_late) > 1 :
            time_filter = transaction_late[0].get('date_display')
            _created_time = transaction_late[0].get('created_time')
        else:
            time_filter = ''

        back_end_url = os.getenv('URL_PREFIX')
        url = f'{back_end_url}/v1/transaction/trans-installment/report'
        payload={
            "odoo_contact_id": str(_id),
            "time_filter" : time_filter
        }

        # headers = {}
        response = requests.post(url, json=payload)
        _data = response.json().get('data')
        if _data is not None:
            _list_transaction = _data.get('transactions')
            for trans in _list_transaction:
                if _created_time != trans.get('created_time'):
                    time_string = datetime.datetime.fromtimestamp(trans.get('created_time')).strftime('%d/%m/%YT%H:%M:%S%z')

                    self.env['transaction.installment'].create({
                        'date_trans': trans.get('created_time'),
                        'bank' : trans.get('installment_bank'),
                        'date_display' : time_string,
                        'card_organization': trans.get('card_organization'),
                        'name_card': trans.get('name'),
                        'card_number': trans.get('card_number'),
                        'total_amount': trans.get('total_amount'),
                        'period': trans.get('period'),
                        'identity_card': trans.get('identity_card'),
                        'approve_code': trans.get('approve_code'),
                        'phone': trans.get('phone'),
                        'contact_id': _id
                    })
        else:
            return
