from datetime import datetime

from odoo import api, models, modules, fields, _


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _sql_constraints = [
        ('ref_id_unique', 'unique(ref_id)', 'Mã merchant đã tồn tại')
    ]

    partner_ref_mid = fields.One2many('res.partner.ref_mid_code','partner_id', string='MID/REF CODE')