from odoo import fields, models, api


class AccountPosMachines(models.Model):
    _name = 'account.pos.machines'
    _rec_name = 'username'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    _description = 'Pos machines'

    # product lot
    # product_lot = fields.Many2one(
    #     'stock.production.lot', 'Máy',
    #     states={'active': [('readonly', True)]})

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', readonly=True)

    username = fields.Char(
        string="Account",
        states={'active': [('readonly', True)]}
    )

    partner_id = fields.Many2one('res.partner', string="Merchant")

    # stock line
    stock_move_line = fields.Many2one('stock.move.line',
                                      string='Phiếu xuất kho'
                                      )

    states = fields.Selection(selection='get_states_options', string='Trạng thái máy', tracking=True)

    @api.model
    def get_states_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'states'), ('model', '=', 'pos.machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    counter = fields.Char(string='Quầy', tracking=True)
    floor = fields.Char(string='Tầng', tracking=True)
    house_number = fields.Char(string='Số nhà', tracking=True)
    street = fields.Char(string='Đường', tracking=True)
    zip = fields.Char(string='Mã Zip', tracking=True)
    city = fields.Char(string='Thành phố', tracking=True)
