
from odoo import api, fields, models


class TidRate(models.Model):

    _name = "mms.tid_rate"
    #_inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = "tid rate management"

    cost_rate = fields.Float('cost rate', required=True, tracking=True)
    
    cogs_rate = fields.Float('cogs rate', required=True, tracking=True)

    card_type = fields.Selection(selection='get_card_type_options', string='Loại thẻ', tracking=True)
        
    status = fields.Selection(selection='get_status_options', string='Trạng thái máy', tracking=True)

    @api.model
    def get_status_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'status'), ('model', '=', 'pos_machines')])
        return [(x.get('value'), x.get('name')) for x in options]
        
    tid_id = fields.Many2one('mms.tid', string='mã tid', required=True)
    
