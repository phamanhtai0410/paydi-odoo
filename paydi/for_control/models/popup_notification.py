from odoo import fields, models, api

class PopupNotification(models.Model):
    _name = 'popup.notification'
    _description = 'Description'

    message = fields.Text('Message', required=True)

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}