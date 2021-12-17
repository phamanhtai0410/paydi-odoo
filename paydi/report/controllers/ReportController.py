
from sys import path_hooks
from odoo import http
from odoo.http import request
import requests
import json
from datetime import datetime
from ..enums.customer_reports import CARD_TYPES, CUSTOMER_REPORT_TYPES, CUSTOMER_REPORT_OID, TRANSACTION_TYPE
from ..enums.transactions import TRANSACTION_TYPE, TRANSACTION_STATUS
from config import DefaultConfig
import boto3
import uuid
from botocore.exceptions import ClientError
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

    # ----------------------------------------------------------------------------------------------------
    ######################################################################################################

    @http.route('/report/transactions/', website=True, auth='public')
    def report_transactions(self, **kw):
        return request.render("report.list_transactions_page")


    @http.route('/report/transactions/data/transactions/', website=False, auth='public', methods=['GET'], csrf=False, type="http")
    def get_transactions(self, **kw):
        print(' -+= DataTable GET data = ', kw)
        responseGetListTransactions = requests.get(
            DefaultConfig.url_prefix + '/v1/data-odoo/transactions_statistic/transactions', 
            headers={}
        ) 
        transactions = responseGetListTransactions.json().get('data').get('transactions')
        transactions = [
            {
                'obj_type': TRANSACTION_TYPE.get(transaction.get('obj_type')),
                'status': TRANSACTION_STATUS.get(transaction.get('status')) if transaction.get('status') == 'success' else 'Failed',
                'total_amount': '{:,.2f}'.format(transaction.get('total_amount')) + ' VNĐ',
                'error_msg': transaction.get('error_msg'),
                'created_time': datetime.fromtimestamp(transaction.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                'extract': transaction.get('extract')
            }
            for transaction in transactions
        ]
        
        total = responseGetListTransactions.json().get('data').get('total')

        print("-+= responseGetListTransactions", transactions)
        return  json.dumps({
            'data': transactions,
            'total': total
        })


    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
    @http.route(['/report/customer_report', '/report/customer_report/page/<int:page>'], auth="user", website=True, type="http")
    def get_list_customer_report(self, page=0, **post):

        responseGetTotalReports = requests.get(
            DefaultConfig.url_prefix + '/v1/support/report/get_list_for_admin?limit={}&offset={}'.format(10, 0), 
            headers={}
        )
        
        total = responseGetTotalReports.json().get('data').get('total')
        print('total = ', total)
        limit = 10

        pager = request.website.pager(
            url='/report/customer_report',
            total=total,
            page=page,
            step=limit,
        )

        offset = pager['offset']

        responseGetListReport = requests.get(
            DefaultConfig.url_prefix + '/v1/support/report/get_list_for_admin?limit={}&offset={}'.format(limit, offset), 
            headers={}
        )

        print('limit =', limit)
        print('offset =', offset)
        print('response get List report =', responseGetListReport.json())
        

        reports = responseGetListReport.json().get('data').get('reports')

        reports = [
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
                    'created_time': datetime.fromtimestamp(report.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                }
                for report in reports
            ]
        print('-+-  responseGetListReport', reports)

        return request.render("report.list_customer_reports_page", {
            'reports': reports,
            'pager': pager,
            'total': total,
            'from_index': offset + 1,
            'to_index': offset + limit,
            'limit': limit,
            'offset': offset,
        })


    @http.route('/report/bank_pos_logs', auth="user", website=True, type="http")
    def get_list_bank_pos_logs(self, **kw):

        ## Config s3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=DefaultConfig.S3_KEY,
            aws_secret_access_key=DefaultConfig.S3_SECRET,
            endpoint_url=DefaultConfig.S3_ENDPOINT,
            use_ssl=False,
        )

        ## 
        def get_list_objects_by_path(path):
            try:
                return s3.list_objects_v2(Bucket=DefaultConfig.S3_BUCKET, Prefix=f'{path}')
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    return None

        path = 'log/bank'

        bank_logs = get_list_objects_by_path(path)
       
        bank_logs = [
                {
                    'url': DefaultConfig.S3_URL + log.get('Key'),
                    'size': log.get('Size'),
                    'last_modified': log.get('LastModified').strftime("%d/%m/%Y, %H:%M:%S"),
                    'etag': log.get('ETag'),
                    'storage_class': log.get('StorageClass')
                }
                for log in bank_logs['Contents']
            ]
            
        bank_logs.reverse()


        ###



        return request.render("report.list_bank_pos_logs_page", {
            'bank_logs': bank_logs
        })