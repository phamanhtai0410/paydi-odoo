from odoo import fields, models, api
import base64
from io import StringIO
from xlrd import open_workbook
# import xlrd

class ForControl(models.TransientModel):
    _name = 'for.control'
    _description = 'Description'
    _rec_name = 'name'
    
    model = fields.Char(string="Đối tượng")
    field = fields.Char(string="Trường dữ liệu")
    value = fields.Char(string="Giá trị")
    name = fields.Char(string="Hiển thị")

    # import_data_form_file = fields.Binary(string='Upload File')
    bank = fields.Selection([ ('tpbank', 'TP Bank'),('vietcombank', 'Vietcombank'),('BIDV','Đã cấp máy')],'Ngân hàng', default='tpbank')
    spending_account = fields.Selection([ ('123456789', '123456789'),('132654987', '132654987')],'Tài khoản chi', default='123456789')
    method = fields.Selection([ ('noi dia', 'Nội địa'),('quoc te', 'Quốc tế')],'Phương thức thanh toán', default='noi dia')

    # file_name = fields.Binary(string='Upload File')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')

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

    @api.onchange('file_data')
    def _onchange_shape(self):
        print("-------------------seft------------------", self.file_name)
        print("-------------------input file------------------", self.file_data)
        # wb = open_workbook(file_contents = base64.decodestring(self.file_name))
        # sheet = wb.sheets()[0]
        # print('sheettttttttt =================', sheet)
        #Decode data
        if self.file_name:
            data = base64.b64decode(self.file_data)
            #Save file
            with open('/tmp/' + self.file_name, 'wb') as file:
                file.write(data)
            xl_workbook = open_workbook(file.name)
            sheet_names = xl_workbook.sheet_names()
            xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
            num_cols = xl_sheet.ncols
            print('----------------------num_cold---------------------', num_cols)

            headers = []
            for col_idx in range(0, num_cols):
                cell_obj = xl_sheet.cell(0, col_idx)
                headers.append(cell_obj.value)

            import_data = []
            for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows
                row_dict = {}
                for col_idx in range(0, num_cols):  # Iterate through columns
                    cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
                    row_dict[headers[col_idx]] = cell_obj.value
                import_data.append(row_dict)
            print('-----------------------import_data ----------------', import_data)

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

    
    
    
