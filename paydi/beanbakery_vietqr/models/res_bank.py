from odoo import fields, models, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    code = fields.Char('Code')
    short_name = fields.Char('Short Name')
    logo_url = fields.Char('Link Url')
    transfer_supported = fields.Boolean("Transfer Supported")
    lookup_supported = fields.Boolean("Lookup Supported")
    swift_code = fields.Char('Swift Code')
    
    
