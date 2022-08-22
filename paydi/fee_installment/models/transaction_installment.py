from odoo import fields, models, api

class TransactionInstallment(models.Model):
    _name = 'transaction.installment'
    _description = 'Description'
    _order = 'date_trans desc'

    date_trans = fields.Float(string="date_trans")
    bank = fields.Char(string="Ngân hàng")
    card_organization = fields.Char(string="Loại thẻ")
    name_card = fields.Char(string="Họ và tên chủ thẻ")
    card_number = fields.Char(string="Số thẻ của chủ thẻ")
    total_amount = fields.Float(string="Số tiền đăng ký trả góp")
    period = fields.Integer(string="Kỳ hạn")
    identity_card = fields.Char(string="Giấy tờ tùy thân")
    approve_code = fields.Char(string="Approval code")
    phone = fields.Char(string="Số điện thoại")
    date_display = fields.Char('Ngày bắt đầu')
    contact_id = fields.Many2one(comodel_name="res.partner", string="contact id", required='1')