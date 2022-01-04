
from logging import error
from sys import path_hooks
# from odoo import http
from odoo.http import request
import odoo.http as http
import requests
import json
from datetime import datetime
from ..enums.customer_reports import CARD_TYPES, CUSTOMER_REPORT_TYPES, CUSTOMER_REPORT_OID
from ..enums.transactions import TRANSACTION_TYPE, TRANSACTION_STATUS
from config import DefaultConfig
import boto3
import uuid
from botocore.exceptions import ClientError
import re
# common header





class TransactionController(http.Controller):

    @staticmethod
    def get_company_id_of_tranx(odoo_contact_id: str):
        contact = http.request.env['res.partner'].sudo().search([('id', '=', odoo_contact_id)]).read()
        if len(contact):  
            return contact[0].get('company_id')
        else:
            return None
       
    @staticmethod 
    def check_odoo_contact_id(odoo_contact_id: str):
        contact = http.request.env['res.partner'].sudo().search([('id', '=', odoo_contact_id)]).read()
        return len(contact)
    
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

    # ----------------------------------------------------------------------------------------------------
    ######################################################################################################
    
    @http.route('/report/transactions/data/transactions/', website=False, auth='public', methods=['GET'], csrf=False, type="http")
    def get_transactions(self, **kw):
        
        ###############################################################
        #                           Transactions
        ###############################################################
        # print('get Transactions kw = ', kw)
        print('----------- -----------')
        print('DataTables List Transactions opitons : ', kw)
        
        type_search_value = kw.get('columns[2][search][value]')
        status_search_value = kw.get('columns[3][search][value]')

        isInType = False
        isInStatus = False
        
        if type_search_value:
            for key, val in TRANSACTION_TYPE.items():
                if type_search_value:
                    if re.search(type_search_value.lower(), val.lower()):
                        type_search_value = key
                        isInType = True
                        break
            print('After - Type : ', isInType, ' and : ', type_search_value)
            
        if status_search_value:
            for key, val in TRANSACTION_STATUS.items():
                if status_search_value:
                    if re.search(status_search_value.lower(), val.lower()):
                        status_search_value = key
                        isInStatus = True
                        break
            print('After - Status : ', isInStatus,  'and : ', status_search_value)
            
        
        if type_search_value or status_search_value:
            if not isInStatus and not isInType:
                return json.dumps({
                                'draw': kw.get('draw'),
                                'data': {},
                                'total': 0,
                                'start': kw.get('start'),
                                'length': kw.get('length')
                            })
        
        responseGetListTransactions = requests.get(
            DefaultConfig.url_prefix + 
            '/v1/data-odoo/transactions_statistic/transactions?offset={}&limit={}&search_type={}&search_status={}'
            .format(kw.get('start'), kw.get('length'), type_search_value, status_search_value), 
            headers={
                
            }
        ) 
        
        transactions = responseGetListTransactions.json().get('data').get('transactions')
          
        transactions = [
            {
                '_id': transaction.get('_id'),
                'pos_id': transaction.get('pos_id'),
                'obj_type': TRANSACTION_TYPE.get(transaction.get('obj_type')),
                'status': TRANSACTION_STATUS.get(transaction.get('status')) if transaction.get('status') == 'success' or transaction.get('status') == 'pending' else 'Failed',
                'total_amount': '{:,.2f}'.format(transaction.get('total_amount')) + ' VNĐ',
                'error_msg': transaction.get('error_msg'),
                'created_time': datetime.fromtimestamp(transaction.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                'extract': transaction.get('extract'),
                'contact': transaction.get('odoo_contact_id') if TransactionController.check_odoo_contact_id(transaction.get('odoo_contact_id')) else -1,
                'company_id': TransactionController.get_company_id_of_tranx(transaction.get('odoo_contact_id')),
                'has_voided': transaction.get('has_voided')
            }
            for transaction in transactions
        ]
        
        total = responseGetListTransactions.json().get('data').get('total')
              
        # --------------------------------------------------------
        
        return  json.dumps({
            'draw': kw.get('draw'),
            'data': transactions,
            'total': total,
            'start': kw.get('start'),
            'length': kw.get('length')
        })


    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
    
    @http.route('/report/transactions/data/error_transactions/', website=False, auth='public', methods=['GET'], csrf=False, type="http")
    def get_error_transactions(self, **kw):
        
        ###############################################################
        #                    Error Transactions
        ###############################################################
        
        print('DataTables List Error Transactions opitons : ', kw)
        
        app_ver_search_value = kw.get('columns[2][search][value]')
        code_search_value = kw.get('columns[3][search][value]')
        description_search_value = kw.get('columns[4][search][value]')
        bank_code_search_value = kw.get('columns[1][search][value]').upper()
        
        responseGetListErrorTransactions = requests.get(
            DefaultConfig.url_prefix + 
            '/v1/data-odoo/transactions_statistic/error_transactions?offset={}&limit={}&search_app_ver={}&search_code={}&search_description={}&search_bank_code={}'
            .format(kw.get('start'),
                    kw.get('length'),
                    app_ver_search_value,
                    code_search_value,
                    description_search_value,
                    bank_code_search_value),
            headers={}
        )
        
        error_transactions = responseGetListErrorTransactions.json().get('data').get('transactions')
        
        error_transactions = [ 
            {
                "account_id": transaction.get("account_id"),
                "app_ver": transaction.get("app_ver", ""),
                "card_holder": transaction.get("card_holder"),
                "card_number": transaction.get("card_number"),
                "code": transaction.get("code", ""),
                "created_time": datetime.fromtimestamp(transaction.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                "desc": transaction.get("desc", ""),                
                "exp_date": transaction.get("exp_date"),
                "pos_id": transaction.get("pos_id"),
                "req_acqr_id": transaction.get("req_acqr_id"),
                "req_card_type": transaction.get("req_card_type"),
                "req_currency_name": transaction.get("req_currency_name"),
                "req_merchant_trans_id": transaction.get("req_merchant_trans_id"),
                "req_tip_amount": '{:,.2f}'.format(transaction.get('req_tip_amount')),
                "req_transaction_amount": '{:,.2f}'.format(transaction.get('req_transaction_amount')),
                "req_tranx_type": transaction.get("req_tranx_type"),
                "swipe_type": transaction.get("swipe_type"),
                "tranx_type": transaction.get("tranx_type", ""),
                'contact': transaction.get('odoo_contact_id') if TransactionController.check_odoo_contact_id(transaction.get('odoo_contact_id')) else -1,
                'company_id': TransactionController.get_company_id_of_tranx(transaction.get('odoo_contact_id')),
                'bank_code': transaction.get('bank_code') if transaction.get('bank_code') else 'None'
            }
            for transaction in error_transactions
        ]
        
        error_total = responseGetListErrorTransactions.json().get('data').get('total')
       
        # --------------------------------------------------------
        
        return  json.dumps({
            'draw': kw.get('draw'),
            'data': error_transactions,
            'total': error_total,
            'start': kw.get('start'),
            'length': kw.get('length')
        })


    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
    @http.route('/report/transactions/data/card_transactions/', website=False, auth='public', methods=['GET'], csrf=False, type="http")
    def get_card_transactions(self, **kw):
        
        ###############################################################
        #                   Card Transactions
        ###############################################################
        print('DataTables List Card Transactions opitons : ', kw)
        
        batch_no_search_value = kw.get('columns[2][search][value]')
        app_ver_search_value = kw.get('columns[6][search][value]')
        code_search_value = kw.get('columns[7][search][value]')
        description_search_value = kw.get('columns[9][search][value]')
        tranx_type_search_value = kw.get('columns[10][search][value]')
        bank_code_search_value = kw.get('columns[5][search][value]').upper()
        
        responseGetListCardTransactions = requests.get(
            DefaultConfig.url_prefix +
            '/v1/data-odoo/transactions_statistic/card_transactions?offset={}&limit={}&search_batch_no={}&search_app_ver={}&search_code={}&search_description={}&search_tranx_type={}&search_bank_code={}'
            .format(kw.get('start'),
                    kw.get('length'),
                    batch_no_search_value,
                    app_ver_search_value,
                    code_search_value,
                    description_search_value,
                    tranx_type_search_value,
                    bank_code_search_value),
            headers={}
        )
        card_transactions = responseGetListCardTransactions.json().get('data').get('transactions')
        card_transactions = [ 
            {
                "account_id": transaction.get("account_id"),
                "app_ver": transaction.get("app_ver", ""),
                "approve_code": transaction.get("approve_code"),
                "bank_merchant_id": transaction.get("bank_merchant_id"),
                "batch_no": transaction.get("batch_no"),
                "card_holder": transaction.get("card_holder"),
                "card_number": transaction.get("card_number"),
                "card_type": transaction.get("card_type"),
                "code": transaction.get("code", ""),
                "created_time": datetime.fromtimestamp(transaction.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                "currency": transaction.get("currency"),
                "desc": transaction.get("desc", ""),
                "exp_date": transaction.get("exp_date"),
                "invoice_no": transaction.get("invoice_no"),
                "iso_response_code": transaction.get("iso_response_code"),
                "merchant_trans_id": transaction.get("merchant_trans_id"),
                "pos_id": transaction.get("pos_id"),
                "ref_no": transaction.get("ref_no"),
                "req_acqr_id": transaction.get("req_acqr_id"),
                "req_card_type": transaction.get("req_card_type"),
                "req_currency_name": transaction.get("req_currency_name"),
                "req_merchant_trans_id": transaction.get("req_merchant_trans_id"),
                "req_tip_amount": '{:,.2f}'.format(transaction.get("req_tip_amount")),
                "req_transaction_amount": '{:,.2f}'.format(transaction.get("req_transaction_amount")),
                "req_tranx_type": transaction.get("req_tranx_type"),
                "swipe_type": transaction.get("swipe_type"),
                "terminal_id": transaction.get("terminal_id"),
                "total_amount": '{:,.2f}'.format(transaction.get('total_amount')),
                "trace_no": transaction.get("trace_no"),
                "trans_date_time": datetime.fromtimestamp(transaction.get('trans_date_time')).strftime("%d/%m/%Y, %H:%M:%S"),
                "tranx_type": transaction.get("tranx_type"),
                'contact': transaction.get('odoo_contact_id') if TransactionController.check_odoo_contact_id(transaction.get('odoo_contact_id')) else -1,
                'company_id': TransactionController.get_company_id_of_tranx(transaction.get('odoo_contact_id')),
                'bank_code': transaction.get('bank_code') if transaction.get('bank_code') else 'None'
            }
            for transaction in card_transactions
        ]
        card_total = responseGetListCardTransactions.json().get('data').get('total')
      
        # --------------------------------------------------------
        
        return  json.dumps({
            'draw': kw.get('draw'),
            'data': card_transactions,
            'total': card_total,
            'start': kw.get('start'),
            'length': kw.get('length')
        })


    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
     
    @http.route('/report/transactions/data/pre_auth_transactions/', website=False, auth='public', methods=['GET'], csrf=False, type="http")
    def get_pre_auth_transactions(self, **kw):
        
        ###############################################################
        #                    Pre-Auth Transactions
        ###############################################################
        print('DataTables List Pre-Auth Transactions opitons : ', kw)
        bank_code_search_value = kw.get('columns[2][search][value]').upper()
        invoice_no_search_value = kw.get('columns[3][search][value]')
        has_voided_search_value = kw.get('columns[4][search][value]')
        
        responseGetListPreAuthTransactions = requests.get(
            DefaultConfig.url_prefix +
            '/v1/data-odoo/transactions_statistic/pre_auth_transactions?offset={}&limit={}&search_invoice_no={}&search_has_voided={}&search_bank_code={}'
            .format(kw.get('start'),
                    kw.get('length'),
                    invoice_no_search_value,
                    has_voided_search_value,
                    bank_code_search_value),
            headers={}
        )
        pre_auth_transactions = responseGetListPreAuthTransactions.json().get('data').get('transactions')
        pre_auth_transactions = [ 
            {
                "_id": transaction.get('_id'),
                "account_id": transaction.get("account_id"),
                "app_ver": transaction.get("app_ver", ""),
                "approve_code": transaction.get("approve_code", ""),
                "bank_merchant_id": transaction.get("bank_merchant_id", ""),
                "batch_no": transaction.get("batch_no", ""),
                "card_holder": transaction.get("card_holder"),
                "card_number": transaction.get("card_number"),
                "card_type": transaction.get("card_type"),
                "code": transaction.get("code"),
                "created_time": datetime.fromtimestamp(transaction.get('created_time')).strftime("%d/%m/%Y, %H:%M:%S") if isinstance(transaction.get('created_time'), int) else '',
                "currency": transaction.get("currency"),
                "desc": transaction.get("desc"),
                "exp_date": transaction.get("exp_date"),
                "has_voided": transaction.get("has_voided"),
                "invoice_no": transaction.get("invoice_no"),
                "iso_response_code": transaction.get("iso_response_code"),
                "merchant_trans_id": transaction.get("merchant_trans_id"),
                "odoo_contact_id": transaction.get("odoo_contact_id"),
                "pos_id": transaction.get("pos_id"),
                "ref_no": transaction.get("ref_no"),
                "req_acqr_id": transaction.get("req_acqr_id"),
                "req_card_type": transaction.get("req_card_type"),
                "req_currency_name": transaction.get("req_currency_name"),
                "req_merchant_trans_id": transaction.get("req_merchant_trans_id"),
                "req_tip_amount": '{:,.2f}'.format(transaction.get('req_tip_amount')) if isinstance(transaction.get('req_tip_amount'), float) else '',
                "req_transaction_amount": '{:,.2f}'.format(transaction.get("req_transaction_amount")) if isinstance(transaction.get('req_transaction_amount'), float) else '',
                "req_tranx_type": transaction.get("accoureq_tranx_typent_id"),
                "section_no": transaction.get("section_no"),
                "swipe_type": transaction.get("swipe_type"),
                "terminal_id": transaction.get("terminal_id"),
                "total_amount": '{:,.2f}'.format(transaction.get("total_amount")) if isinstance(transaction.get('total_amount'), float) else '',
                "trace_no": transaction.get("trace_no", ""),
                "trans_date_time": datetime.fromtimestamp(transaction.get('trans_date_time')).strftime("%d/%m/%Y, %H:%M:%S") if isinstance(transaction.get('trans_date_time'), int) else transaction.get('trans_date_time'),
                "tranx_type": transaction.get("tranx_type"),
                "void_data": transaction.get("void_data"),
                'contact': transaction.get('odoo_contact_id') if TransactionController.check_odoo_contact_id(transaction.get('odoo_contact_id')) else -1,
                'company_id': TransactionController.get_company_id_of_tranx(transaction.get('odoo_contact_id')),
                'bank_code': transaction.get('bank_code') if transaction.get('bank_code') else 'None'
            }
            for transaction in pre_auth_transactions
        ]
        pre_auth_total = responseGetListPreAuthTransactions.json().get('data').get('total')
        
        # --------------------------------------------------------
        
        return  json.dumps({
            'draw': kw.get('draw'),
            'data': pre_auth_transactions,
            'total': pre_auth_total,
            'start': kw.get('start'),
            'length': kw.get('length')
        })


    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
    
    @http.route(['/report/customer_report', '/report/customer_report/page/<int:page>'], auth="user", website=True, type="http")
    def get_list_customer_report(self, page=0, **post):

        responseGetTotalReports = requests.get(
            DefaultConfig.url_prefix + '/v1/data-odoo/report/get_list_for_admin?limit={}&offset={}'.format(10, 0), 
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
            DefaultConfig.url_prefix + '/v1/data-odoo/report/get_list_for_admin?limit={}&offset={}'.format(limit, offset), 
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

    #----------------------------------------------------------------------------------------------------
    #####################################################################################################
    
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