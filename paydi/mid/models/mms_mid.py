
from odoo import api, fields, models


class Mid(models.Model):

    _name = "mms.mid"

    code = fields.Char('mid code', translate=True, required=True)
    
    mid_master_code = fields.Char('mid master code', translate=True)
    
    status = fields.Char('status', translate=True, required=True)

    partner_id = fields.Many2one('res.partner', string='Hồ sơ')
    
    tid = fields.One2many('mms.tid', 'tid',  string='Mã mid')
