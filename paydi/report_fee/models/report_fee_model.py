from datetime import datetime
from importlib.resources import path
import json
import time
import os
import requests
from odoo import api, models, modules, fields, _
from odoo.http import request
from odoo import http
from urllib.parse import urlparse
from urllib.parse import parse_qs

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    fromdate = fields.Datetime('From date')
    todate = fields.Datetime('To date')

    def export_action_withdate(self,arg):        
        fromdate_res = datetime.strptime(arg["fromdate"], "%Y-%m-%d").strftime("%d/%m/%Y")
        todate_res = datetime.strptime(arg["todate"], "%Y-%m-%d").strftime("%d/%m/%Y")

        url = arg['crr_url']
        uri = urlparse(url)
        qs = uri.fragment
        ids = int(parse_qs(qs).get('id', None)[0])

        records = self.env["res.partner.fee"].search_read([("partner_id","=",ids)])
        print('--------------------records-------------------------', records)


        if len(records) < 1:
            fees = []
            return {
                'url' : False
            }
        else :
            fees = []
            # {
                #     "odoo_contact_id": 9, 
                #     "merchant_name": "Công ty Cổ Phần Thương Mại Dịch Vụ Trà Cà Phê VN - The Coffee House", 
                #     "card_type": 3, 
                #     "bank": "EIB", 
                #     "fee": 1.6, 
                #     "from_date": 1603245266.0, 
                #     "to_date": 1651894469.0
                #     }
                # types = {
                #     '1': 'VISA/JCB',
                #     '2': 'NAPAS',
                #     '3': 'MasterCard'
                # }   
            for record in records:
                if record.get('card_type') == False or record.get('bank') == False or record.get('fee') == False or record.get('from_date') == False or record.get('to_date') == False:
                    return {
                        'url' : 'not_value'
                    } 
                if record.get('card_type') == 'VISA/JCB': _card_type = 1
                elif record.get('card_type') == 'NAPAS': _card_type = 2
                else : _card_type = 3

                record_obj = {
                    'odoo_contact_id' : record.get('partner_id')[0],
                    'merchant_name':record.get('partner_id')[1],
                    'card_type' : _card_type,
                    'bank': record.get('bank')[1],
                    'fee': record.get('fee'),
                    'from_date': time.mktime(record.get('from_date').timetuple()),
                    'to_date': time.mktime(record.get('to_date').timetuple())
                }
                fees.append(record_obj)

        fee_obj = {
            "fromdate_res" : fromdate_res,
            "todate_res" : todate_res,
            "fees_by_time" : fees
        }

        back_end_url = os.getenv('URL_ODOO_SV')
        url = f'{back_end_url}/v1/data-odoo/transactions_statistic/report_transactions_by_time'
        result = requests.post(url, json=fee_obj)
        path = result.json().get('data').get('path')
        return {
            'name': 'TO MODEL C',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': path,
        }

    def export_action(self):
        id = self.ids
        records = self.env["res.partner.fee"].search_read([("partner_id","=",id[0])])
        if len(records) < 1:
            fees = []
            return
        else :
            fees = []
            for record in records:
                record_obj = {
                'odoo_contact_id' : record.get('partner_id')[0],
                'merchant_name':record.get('partner_id')[1],
                'card_type' : record.get('card_type'),
                'bank': record.get('bank')[1],
                'fee': record.get('fee'),
                'from_date': time.mktime(record.get('from_date').timetuple()),
                'to_date': time.mktime(record.get('to_date').timetuple())
                }
                fees.append(record_obj)
            print(record)
        fee_obj = {
            "fees": fees
        }
        
        back_end_url = os.getenv('URL_ODOO_SV')
        url_report = f'{back_end_url}/v1/data-odoo/transactions_statistic/report_transactions'
        result = requests.post(url_report, json=fee_obj)

        path = result.json().get('data').get('path')
        return {
            'name': 'TO MODEL B',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': path,
        }