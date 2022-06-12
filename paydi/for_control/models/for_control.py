from odoo import fields, models, api


class ForControl(models.Model):
    _name = 'for.control'
    _description = 'Description'
    _rec_name = 'name'
    
    model = fields.Char(string="Đối tượng")
    field = fields.Char(string="Trường dữ liệu")
    value = fields.Char(string="Giá trị")
    name = fields.Char(string="Hiển thị")

    field_name = fields.Binary(string='Upload File')
    bank = fields.Selection([ ('tpbank', 'TP Bank'),('vietcombank', 'Vietcombank'),('BIDV','Đã cấp máy')],'Ngân hàng', default='tpbank')
    spending_account = fields.Selection([ ('123456789', '123456789'),('132654987', '132654987')],'Tài khoản chi', default='123456789')
    method = fields.Selection([ ('noi dia', 'Nội địa'),('quoc te', 'Quốc tế')],'Phương thức thanh toán', default='noi dia')

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
    def action_from_view(self):
        view_id = self.env.ref('for_control.cross_checking_confirm_view').id
        print('-----------------------------------------------------ids view-----------------------------', self)
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

    
    
    
