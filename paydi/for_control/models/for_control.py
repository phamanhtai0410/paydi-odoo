from hashlib import new
from multiprocessing import context
import os
import string
from tempfile import TemporaryFile
from urllib.parse import parse_qs, urlparse

import openpyxl
import requests
from odoo import fields, models, api
import base64
from io import BytesIO, StringIO
from xlrd import open_workbook

from dotenv import load_dotenv
load_dotenv()

from odoo.exceptions import UserError
# import xlrd

class ForControl(models.Model):
    _name = 'for.control'
    _description = 'Description'
    # _rec_name = 'name'
    

    # file_name = fields.Binary(string='Upload File')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    for_control_id = fields.Integer("id")
    bank_title =  fields.Char('bank title')
    bank_type = fields.Char('bank type')
    stk_bank = fields.Char('stk bank')

    total_record = fields.Char('total')
    status_save_file = fields.Integer('status save')
    data_tree_file = fields.One2many(comodel_name="file.data", string="data file",inverse_name="file_name_id")
    
    def import_file(self):
        if self.file_data:

            data = base64.b64decode(self.file_data)
            with open('/tmp/' + self.file_name, 'wb') as file:
                file.write(data)
            xl_workbook = open_workbook(file.name)
            # sheet_names = xl_workbook.sheet_names()
            back_end_url = os.getenv('URL_PREFIX')
            url = f'{back_end_url}/v1/odoo-api/fund_transfer/upload/transfer_report'
            payload={}
            files=[('file',open('/tmp/' + self.file_name, 'rb'))]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(' response upload file =======', response.json())   
            
            if response.json()['error_code'] == '':
                print('upload file successfully')
                self.status_save_file = 1
            else :
                print('upload file fasle ----')
                message_id = self.env['popup.notification'].create({'message': ("Upload file không thành công, vui lòng kiểm tra lại file !")})
                return {
                    'name': ('False'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'popup.notification',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }
               

            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file_data)), read_only=True)
            ws = wb.active
            sheet = wb['Sheet1']
            self.bank_title = sheet['C3'].value
            self.bank_type = sheet['C5'].value
            self.stk_bank = sheet['F3'].value
    
            total = 0
            if self.status_save_file == 1:
                for record in ws.iter_rows(min_row=8, max_row=None, min_col=None,max_col=None, values_only=True):
                    
                    data_record = record[10]
                    if isinstance(data_record, str):
                        if data_record.find(",") == -1:
                            data_col = "{:,}".format(int(data_record))
                        else:
                            data_col = data_record
                    elif isinstance(data_record, int):
                        data_col = "{:,}".format(data_record)
                    else:
                        data_col = record[10]
                    
                    if record[0] is not None:
                        self.env['file.data'].create({

                            'file_name_id' : self.id,
                                        
                            'STT': record[0],
                                        
                            'MID': record[1],
                                        
                            'name': record[2],

                            'product_name': record[3],

                            'bank_value': record[4],

                            'agency': record[5],

                            'bank_number': record[6],

                            'citab_code': record[7],
                        
                            'bin_code': record[8],

                            'beneficiary': record[9],

                            'totol_amount': data_col,
                        })

                        if record[10] is not None and record[10] != 'Số tiền':
                            if isinstance(record[10], str)and record[10].find(','):
                                amount = int(record[10].replace(",", "")) 
                                total = total + amount
                            else:
                                amount = int(record[10])
                                total = total + amount
                
                self.total_record = "{:,}".format(total)

            else:
                message_id = self.env['popup.notification'].create({'message': ("Upload file không thành công, vui lòng kiểm tra lại file !")})
                return {
                    'name': ('False'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'popup.notification',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }
        # return

    def one_more(self,arg):
        url = arg['crr_url']
        uri = urlparse(url)
        qs = uri.fragment
        ids = int(parse_qs(qs).get('id', None)[0])
        id_url=f'id={ids}'
        path_real = url.replace(id_url, "")
        
        return {
            'name': 'TO MODEL B',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': path_real,
        }   

    def action_from_view(self):

        if self.status_save_file == 1:
            body_obj = {
                "file_name": self.file_name
            }
            back_end_url = os.getenv('URL_PREFIX')

            result = requests.post(f'{back_end_url}/v1/odoo-api/fund_transfer/transfer', json=body_obj)

            if result.json()['data']['result'] == 'success':
                message_id = self.env['popup.notification'].create({'message': ("Chuyển tiền thành công !")})
                return {
                    'name': ('Successfull'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'popup.notification',
                    'res_id': message_id.id,
                    'target': 'new'
                }
            elif result.json()['data']['msg'].find("ConnectTimeoutError") != -1 or result.json()['data']['msg'].find("NewConnectionError") != -1:
                message_id = self.env['popup.notification'].create({'message': ("Connect Timeout Error !")})
                return {
                    'name': ('False'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'popup.notification',
                    'res_id': message_id.id,
                    'target': 'new'
                }

            else:
                message_id = self.env['popup.notification'].create({'message': result.json()['data']['msg']})
                return {
                    'name': ('False'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'popup.notification',
                    'res_id': message_id.id,
                    'target': 'new'
                }

        else :
            print('chuyen tien khong thanh cong')
            message_id = self.env['popup.notification'].create({'message': ("Chuyển tiền không thành công, vui lòng kiểm tra lại file !")})
            return {
                'name': ('False'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'popup.notification',
                'res_id': message_id.id,
                'target': 'new'
            }
    
    def your_test_method(self):
        print('button test ok ')

    def get_all_trans_installment(self):

        form_view_id = self.env.ref("fee_installment.transaction_installment_list").id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installment Report All',
            'res_model': 'transaction.installment',
            'views': [(form_view_id, 'tree')],
            'target': 'current',
            # 'domain': [('contact_id.id','=',self.id)],
            'flags': {'search_view': True, 'action_buttons': True},
        }
    
