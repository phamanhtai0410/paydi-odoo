from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # partner_id = fields.Many2one('res.partner', string='Hồ sơ đăng ký')
    sequence_code = fields.Char(related="picking_type_id.sequence_code")
    return_picking_id = fields.Many2one('stock.picking')
    out_picking_id = fields.Many2one('stock.picking')

    def edit_booking(self):
        view_id = self.env.ref('stock.view_picking_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đặt máy làm hồ sơ',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }

    @api.onchange('move_line_ids_without_package')
    def onchange_move_line_ids_without_package(self):
        print('len(record.move_line_ids_without_package)', len(self.move_line_ids_without_package),
              self.move_line_ids_without_package)
        if len(self.move_line_ids_without_package) > 1 and self.sequence_code == 'BOOKING':
            # self.move_line_ids_without_package = self.onchange_move_line_ids_without_package[0]
            raise ValidationError('Tối đa 1 máy')
