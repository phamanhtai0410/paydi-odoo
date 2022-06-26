from datetime import datetime

from odoo import api, models, modules, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _name = 'res.partner.ref_mid_code'
    _description = 'ref_mid_code'

    partner_id = fields.Many2one('res.partner', string="Merchant")

    bank = fields.Many2one('res.bank')
    mid_code = fields.Char(string='Mã MID')
    ref_code = fields.Char(string='Mã REF CODE')