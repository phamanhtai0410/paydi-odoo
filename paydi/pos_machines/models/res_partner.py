from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    stock_move_line = fields.One2many('stock.move.line', 'holder')

    def get_company_of_current_user(self):
        print('_stock_move_line_context')
        return self.env.user.company_id.id
