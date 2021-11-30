from odoo import fields, models, api


class PosMachineSetting(models.TransientModel):
    _name = 'pos.machine.setting.wizard'

    serial_number = fields.Char(
        string="Số serial",
        readonly=True
    )

    partner = fields.Many2one('res.partner',
                              readonly=True,
                              string="Merchant")
    tid_mid = fields.One2many('pos.machine.tid.mid.wizard', 'pos_setting')

    # tid = fields.Char(string="Mã TID")
    # mid = fields.Char(string="Mã MID")

    def your_test_method(self):
        self.ensure_one()
        print('your_test_method', self)
        return {}
