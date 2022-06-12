from odoo import fields, models, api


class CrossChecking(models.Model):
    _name = 'cross.checking'
    _description = 'Description'

    method_checking = fields.Selection([ ('noi dia', 'Nội địa'),('quoc te', 'Quốc tế')],'Phương thức thanh toán', default='noi dia')

    def your_test_method(self):
        print('button test ok ')