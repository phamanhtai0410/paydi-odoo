from odoo import fields, models, api

class ResPartner(models.Model):
    _name = 'res.bank'
    _inherit = 'res.bank'

    is_installment = fields.Boolean(string="Is Installment", default=False)