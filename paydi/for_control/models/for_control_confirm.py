from odoo import fields, models, api


class ForControlConfirm(models.Model):
    _name = 'for.control.confirm'
    _description = 'Description'
    _rec_name = 'name'
    # _inherit = 'for.control'

    method_test = fields.Selection([ ('noi dia', 'Nội địa'),('quoc te', 'Quốc tế')],'Phương thức thanh toán', default='noi dia')