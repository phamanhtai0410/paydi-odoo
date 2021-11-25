from odoo import fields, models, api


class PosMachines(models.Model):
    _name = 'pos.machines'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Pos machines'

    serial_number = fields.Char(string='Mã máy')

    model = fields.Char(string='Model')

    factory = fields.Selection([
        ('PAX', 'PAX')
    ], string="Hãng sản xuất")

    assets_code = fields.Char(string="Mã tài sản")

    tid = fields.Char(string="Mã TID", tracking=True)
    mid = fields.Char(string="Mã MID", tracking=True)

    status = fields.Selection(selection='get_status_options', string='Trạng thái máy', tracking=True)

    @api.model
    def get_status_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'status'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    warehouse = fields.Selection(selection='get_warehouse_options', string='Kho', tracking=True)

    @api.model
    def get_warehouse_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'warehouse'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    owner = fields.Many2one('res.partner', tracking=True)

    counter = fields.Char(string='Quầy', tracking=True)
    floor = fields.Char(string='Tầng', tracking=True)
    house_number = fields.Char(string='Số nhà', tracking=True)
    street = fields.Char(string='Đường', tracking=True)
    zip = fields.Char(string='Mã Zip', tracking=True)
    city = fields.Char(string='Thành phố', tracking=True)
    country_id = fields.Char()

    pos_account = fields.Char('Tên đăng nhập', tracking=True)

    current_partner = fields.Many2one('res.partner', tracking=True)

    # activities = fields.One2many('pos.activity', 'pos_machine')
