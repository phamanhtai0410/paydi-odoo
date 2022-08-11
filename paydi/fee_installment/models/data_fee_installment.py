from odoo import fields, models, api

class FreeInstallment(models.Model):
    _name = 'fee.installment'
    _description = 'Description'

    bank = fields.Many2one(string='Bank', required='1', comodel_name="res.bank",domain=[("is_installment","!=",False)])
    # period = fields.Integer('Period', required='1')
    period = fields.Selection([ ('3', '3'),('6', '6'),('9', '9'),('12', '12'),], 'Period', default='3')
    fee_installment = fields.Float('Fee Installment', required='1')
    from_date = fields.Date(required='1')
    to_date = fields.Date(required='1')
    merchant_id = fields.Many2one(comodel_name="res.partner", string="merchant id", required='1')
