
from odoo import http
from odoo.http import request
import requests
import json
from datetime import datetime
from ..enums.customer_reports import CARD_TYPES, CUSTOMER_REPORT_TYPES, CUSTOMER_REPORT_OID 
from config import DefaultConfig
# common header





class TransactionController(http.Controller):

    @http.route('/report/', website=True, auth="public") 
    def statictis_report(self, **kw):
        responseLogin = requests.post(
            DefaultConfig.url_prefix + '/v1/auth/pos/login',
            headers={},
            json={
                "name": "pos_dev",
                "password": "123456",
                "serial_number": "test123"
            }
        )
        print("responseLogin", responseLogin.json())
        token = responseLogin.json().get('data').get('token')

        responseGetListTransactions = requests.get(
            DefaultConfig.url_prefix + '/v1/transaction/pos', 
            headers={
                'Authorization': 'Bearer ' + token
            }
        )
        
        transactions = responseGetListTransactions.json().get('data').get('transactions')

        return request.render("report.report_page", {
            'count': len(transactions)
        })


    @http.route('/report/transactions/', website=True, auth='public')
    def report_transactions(self, **kw):

        responseLogin = requests.post(
            DefaultConfig.url_prefix + '/v1/auth/pos/login',
            headers={},
            json={
                "name": "pos_dev",
                "password": "123456",
                "serial_number": "test123"
            }
        )
        print("responseLogin", responseLogin.json())
        token = responseLogin.json().get('data').get('token')

        responseGetListTransactions = requests.get(
            DefaultConfig.url_prefix + '/v1/transaction/pos', 
            headers={
                'Authorization': 'Bearer ' + token
            }
        )
        
        transactions = responseGetListTransactions.json().get('data').get('transactions')
        transactions = [
            {
                'account_id': transaction.get('account_id'),
                'merchant_id': transaction.get('merchant_id'),
                'pos_id': transaction.get('pos_id'),
                'terminal_id': transaction.get('terminal_id'),
                'total_amount': transaction.get('total_amount'),
                'created_time': datetime.fromtimestamp(transaction.get('created_time')),
                'obj_type': transaction.get('obj_type'),
                'card_type': CARD_TYPES[int(transaction.get('card_type'))],
                'currency': transaction.get('currency')
            }
            for transaction in transactions
        ]

        print("responseGetListTransactions", transactions)
        return request.render("report.list_transactions_page", {
            'transactions': transactions,
        })
    
    @http.route('/report/customer_report/', auth="public", website=True)
    def get_list_customer_report(self, **kw):
        responseGetListReport = requests.get(
            DefaultConfig.url_prefix + '/v1/support/report/get_list_for_admin', 
            headers={}
        )
        
        reports = responseGetListReport.json().get('data')
        reports = {
            'total': reports.get('total'),
            'reports': [
                {
                    '_id': report.get('_id'),
                    'account_id': report.get('account_id'),
                    'pos_id': report.get('pos_id'),
                    'terminal_id': report.get('terminal_id') if report.get('terminal_id') != None else 'No TID',
                    'serial_number': report.get('serial_number'),
                    'message': report.get('message'),
                    'images': report.get('images'),
                    'type': CUSTOMER_REPORT_TYPES.get(report.get('type')),
                    'oid': report.get('oid') if report.get('oid') != 'app_oid' else CUSTOMER_REPORT_OID.get('app_oid'),
                    'created_time': report.get('created_time'),
                }
                for report in reports.get('reports')
            ]
        }
        print('-+-  responseGetListReport', reports)
        return request.render("report.list_customer_reports_page", {
            'reports': reports.get('reports'),
            'total': reports.get('total')
        })