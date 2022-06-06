from datetime import datetime
from importlib.resources import path
import json
import time
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
        print("=================================model=====================================")
        fromdate_res = datetime.strptime(arg["fromdate"], "%Y-%m-%d").strftime("%d%m%Y")
        todate_res = datetime.strptime(arg["todate"], "%Y-%m-%d").strftime("%d%m%Y")

        url = arg['crr_url']
        uri = urlparse(url)
        qs = uri.fragment
        ids = int(parse_qs(qs).get('id', None)[0])
        
        print('ids =============', ids)
        print('todate_res =======',todate_res)
        print('fromdate_res ===========',fromdate_res)
        records = self.env["res.partner.fee"].search_read([("partner_id","=",ids)])
        print("=================================records in model=====================================", records)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
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
        
        result = requests.post("https://paydi-staging.rinznetwork.com/v1/data-odoo/transactions_statistic/report_transactions", json=fee_obj)
        # result = requests.post("http://localhost:5000/v1/data-odoo/transactions_statistic/report_transactions", json=fee_obj);
        path = result.json().get('data').get('path')
        return {
            'name': 'TO MODEL B',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': path,
        }