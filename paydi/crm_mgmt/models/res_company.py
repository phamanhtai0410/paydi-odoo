from odoo import fields, models, api


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    crm_url = fields.Char(string='URL của CRM')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    company_code = fields.Char(string='Company Code', readonly=True, compute="_get_company_code")
    
    @api.depends('name')
    def _get_company_code(self):
        for each in self:
            each.company_code  = each.name.lower()
        
    
    