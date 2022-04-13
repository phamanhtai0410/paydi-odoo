
import string
from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = "crm.lead" 
    _inherit = 'crm.lead'

    industry = fields.Many2one('res.partner.industry',
                                #   related='partner_id.industry_id',
                                  string='Ngành hàng')