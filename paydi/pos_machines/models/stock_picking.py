from odoo import fields, models, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    # partner_id = fields.Many2one('res.partner', string='Hồ sơ đăng ký')
    sequence_code = fields.Char(related="picking_type_id.sequence_code")
    #
    # def button_validate(self):
    #     self.ensure_one()
    #     for line in self.move_line_ids:
    #         if line.is_setup and (not line.account or not line.account.id):
    #             raise UserError('Vui lòng cài đặt tài khoản PAYDI member của máy POS')
    #
    #     _res = super().button_validate()
    #     for line in self.move_line_ids:
    #         if line.is_setup:
    #             line.account.setting.send_backend()
    #     return _res
