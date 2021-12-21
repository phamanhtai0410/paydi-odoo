
from odoo import api, fields, models


class Mid(models.Model):

    _name = "mms.mid"
    #_inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = "mid management"



    mid = fields.Char('mid code', required=True)
    
    mid_master_code = fields.Char('mid master code')
    
    partner_id = fields.Many2one('res.partner', string='Hồ sơ')
    
    tid = fields.One2many('mms.tid', 'tid',  string='Mã mid')
    
    status = fields.Selection(selection='get_status_options', string='Trạng thái máy', tracking=True)

    @api.model
    def get_status_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'status'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    
