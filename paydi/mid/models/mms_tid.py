
from odoo import api, fields, models


class Tid(models.Model):

    _name = "mms.tid"
    #_inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = "tid management"

    tid = fields.Char('tid code', translate=True, required=True)
    
    Name = fields.Char('status', translate=True, required=True)
    
    min_rev_default = fields.Char('min revalue default')
    
    status = fields.Char('status', translate=True, required=True)
    
    mid = fields.Many2one('mms.mid', string='mã mid')