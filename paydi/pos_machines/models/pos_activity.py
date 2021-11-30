from odoo import fields, models, api


class PosActivity(models.Model):
    _name = 'pos.activity'
    _description = 'Record history event of POS machines'

    activity = fields.Char()

    pos_machine = fields.Many2one('pos.machines', string='Máy POS')

    partner_id = fields.Many2one('res.partner', string='Hồ sơ')
