
from odoo import api, fields, models


class Tid(models.Model):

    _name = "mms.tid"
    #_inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = "tid management"

    tid = fields.Char('tid code', required=True, tracking=True)
    
    name = fields.Char('name', required=True, tracking=True)
    
    min_rev_default = fields.Integer('min revalue default', tracking=True)
    
    status = fields.Selection(selection='get_status_options', string='Trạng thái máy', tracking=True)

    tid_rate = fields.One2many('mms.tid_rate', 'tid_id',  string='Mã mid')

    @api.model
    def get_status_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'status'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]
        
    mid = fields.Many2one('mms.mid', string='mã mid', required=True)
    
    address = fields.Selection(selection='get_address_options', string='Địa chỉ', tracking=True)

    @api.model
    def get_address_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'address'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]
