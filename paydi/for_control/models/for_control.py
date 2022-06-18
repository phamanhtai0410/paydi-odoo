from tempfile import TemporaryFile

import openpyxl
import requests
from odoo import fields, models, api
import base64
from io import BytesIO, StringIO
from xlrd import open_workbook

from odoo.exceptions import UserError
# import xlrd

class ForControl(models.Model):
    _name = 'for.control'
    _description = 'Description'
    _rec_name = 'name'
    
    model = fields.Char(string="Đối tượng")
    field = fields.Char(string="Trường dữ liệu")
    value = fields.Char(string="Giá trị")
    name = fields.Char(string="Hiển thị")

    STT = fields.Char()
    MID = fields.Char()
    name = fields.Char()
    product_name = fields.Char()
    bank_value = fields.Char()
    agency = fields.Char()
    bank_number = fields.Char()
    citab_code = fields.Char()
    bin_code = fields.Char()
    beneficiary = fields.Char()
    totol_amount = fields.Char()

    # import_data_form_file = fields.Binary(string='Upload File')
    bank = fields.Selection([ ('tpbank', 'TP Bank'),('vietcombank', 'Vietcombank'),('BIDV','Đã cấp máy')],'Ngân hàng', default='tpbank')
    spending_account = fields.Selection([ ('123456789', '123456789'),('132654987', '132654987')],'Tài khoản chi', default='123456789')
    method = fields.Selection([ ('noi dia', 'Nội địa'),('quoc te', 'Quốc tế')],'Phương thức thanh toán', default='noi dia')
    abc = fields.Text(string="test")

    # file_name = fields.Binary(string='Upload File')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    for_control_id = fields.Integer("id")
    bank_title =  fields.Char('bank title')
    bank_type = fields.Char('bank type')
    stk_bank = fields.Char('stk bank')
    # file_name_ok = fields.Many2one(comodel_name='file.data', string='file name ok')

    # attachment_ids = fields.Many2many('ir.attachment', 'for_control', 'Id', 'res_id', 'Attachments')
    # you logic goes here

    data_tree_file = fields.One2many(comodel_name="file.data", string="data file",inverse_name="file_name_id")
    
    def import_file(self):
        print('---ids ===============================', self.ids)
        if self.file_data:

            print("-------------------seft------------------", self.file_name)
            print("-------------------input file------------------", self.file_data)
           
            #Decode data
            
            data = base64.b64decode(self.file_data)
            with open('/tmp/' + self.file_name, 'wb') as file:
                file.write(data)
            xl_workbook = open_workbook(file.name)
            # sheet_names = xl_workbook.sheet_names()

            url = "https://paydi-staging.rinznetwork.com/v1/odoo-api/fund_transfer/upload/transfer_report"

            payload={}
            files=[('file',open('/tmp/' + self.file_name, 'rb'))]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print(response.text)
            
        
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file_data)), read_only=True)
            ws = wb.active
            print('-----------------------sheet------------', wb.sheetnames)
            sheet = wb['Sheet1']
            print(sheet['A3'].value)
            # sheet = excel_document['Sheet1']
            # print(sheet['A4'].value)
            self.bank_title = sheet['C3'].value
            self.bank_type = sheet['C5'].value
            self.stk_bank = sheet['F3'].value
            
            print('-------------------------------wb---------------------------------', wb)
            print('-----------------------------------------aa-------------', ws.iter_rows(min_row=2, max_row=None, min_col=None,max_col=None, values_only=True))
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,max_col=None, values_only=True):
                print('in for ')
            # search if the customer exist else create
                
                # search = self.env['file.data'].search([('name', '=', record[1])])
                
                # if not search:
                        
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

                'totol_amount': record[10],
                        
                })
    
        # return


    def one_more(self):
        print('-----------------------------button upoad file----------------------------')
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://localhost:8071/web#id=&action=133&model=for.control&view_type=form&cids=1&menu_id=95',
            'target': 'self',
            'res_id': self.id,
        }

    # def _get_for_control_ids(self):
    #     print('accccc')
    #     for record in self:
    #         stock_picking_ids = []
    #         if record.stock_book_lines:
    #             for x in record.stock_book_lines:
    #                 stock_picking_ids.append(x.picking_id.id)
    #         record.update({'stock_picking_ids': [(6, 0, stock_picking_ids or [])]})

    # transaction_ids = fields.One2many('for.control')

    # def action_from_view(self, cr, uid, ids, context=None):
    # http://www.numberspeaks.com/2018/05/11/import-xlsx-file-odoo-11-sales-orders/

    # @api.onchange('file_data')
    # def _onchange_shape(self):
    #     print("-------------------seft------------------", self.file_name)
    #     print("-------------------input file------------------", self.file_data)
        
    #     if self.file_name:
    #         data = base64.b64decode(self.file_data)
    #         with open('/tmp/' + self.file_name, 'wb') as file:
    #             file.write(data)
    #         xl_workbook = open_workbook(file.name)
    #         sheet_names = xl_workbook.sheet_names()
    #         xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
    #         num_cols = xl_sheet.ncols

    #         headers = []
    #         for col_idx in range(0, num_cols):
    #             cell_obj = xl_sheet.cell(6, col_idx)
    #             headers.append(cell_obj.value)
    #         print('-----------------------import_data ----------------', headers)

    #         import_data = []
    #         for row_idx in range(7, xl_sheet.nrows):    # Iterate through rows
    #             row_dict = {}
    #             for col_idx in range(0, num_cols):  # Iterate through columns
    #                 cell_obj = xl_sheet.cell( row_idx,col_idx)  # Get cell object by row, col
    #                 row_dict[headers[col_idx]] = cell_obj.value
    #             import_data.append(row_dict)
    #             print('----------------------cell_obj.value---------------------', import_data)
    #         self.abc = str(import_data)

    def action_from_view(self):
        view_id = self.env.ref('for_control.cross_checking_confirm_view').id
        print('-----------------------------ids view-----------------------------', self)
        print('view_id', view_id)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cross.checking',    
            'views': [(view_id, 'form')], 
            'view_id': view_id, 
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }

    
    
    
