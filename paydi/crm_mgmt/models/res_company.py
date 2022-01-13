from odoo import fields, models, api


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    crm_url = fields.Char(string='URL của CRM')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')