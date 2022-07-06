from odoo import models

class ResPartner(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    _description = "Stock Move"