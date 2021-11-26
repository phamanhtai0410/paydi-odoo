
from odoo import api, fields, models, _


class Mid(models.Model):

    _name = "mms.mid"
    _description = "mid management"
    _order = 'sequence'

    # id = fields.Char('mid id', translate=True, required=True)
    code = fields.Char('mid code', translate=True, required=True)
    mid_master_code = fields.Char('mid master code', translate=True, required=True)
    status = fields.Char('status', translate=True, required=True)

    partner_id = fields.Many2one('res.partner', string='Hồ sơ')