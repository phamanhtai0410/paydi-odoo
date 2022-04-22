from datetime import datetime
import json
import time
import requests
import webbrowser
from odoo import api, models, modules, fields, _
from odoo.http import request

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
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
            
        fee_obj = {
            "fees": fees
        }
        
        result = requests.post("https://paydi-staging.rinznetwork.com/v1/data-odoo/transactions_statistic/report_transactions", json=fee_obj);
        # result = requests.post("http://localhost:5000/v1/data-odoo/transactions_statistic/report_transactions", json=fee_obj);
        path = result.json().get('data').get('path')
        print('================================path==============================', path)
        # webbrowser.open_new_tab(path)
        webbrowser.open(path)
        return True