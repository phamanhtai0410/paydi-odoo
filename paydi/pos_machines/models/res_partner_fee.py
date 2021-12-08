from odoo import fields, models, api


class ResPartnerFee(models.Model):
    _name = 'res.partner.fee'
    _description = 'Fee'

    partner_id = fields.Many2one('res.partner', string="Merchant", readonly=True)
    card_type = fields.Char(string='Lọa thẻ')
    bank = fields.Char(string='Ngân hàng')
    fee = fields.Float(string='Mức phí')
    from_date = fields.Datetime(string='Bắt đầu từ')
    active = fields.Boolean(string='Hiệu lực', default=False)
    industry_id = fields.Many2one('res.partner.industry', string='Ngành hàng', readonly=True)
