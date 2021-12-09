from datetime import datetime

from odoo import api, models, modules, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _sql_constraints = [
        ('ref_id_unique', 'unique(ref_id)', 'Mã merchant đã tồn tại')
    ]

    ref_id = fields.Char()

    partner_fee_ids = fields.One2many('res.partner.fee', 'partner_id', string='Phí máy')

    def _get_ref_view(self):
        print('_get_ref_id', self)
        for record in self:
            record.ref_view = 'Nhập mã'
            if record.ref_id and 'default-' not in record.ref_id:
                record.ref_view = record.ref_id

    def _set_ref_view(self):
        for record in self:
            if record.ref_view and record.ref_view != 'Nhập mã':
                record.ref_id = record.ref_view

    ref_view = fields.Char(compute='_get_ref_view', inverse='_set_ref_view')
    picking_id = fields.Many2one('stock.picking', readonly=True)

    stock_out_picking_id = fields.Many2one('stock.picking',
                                           string="Phiếu xuất kho",
                                           readonly=True)

    picking_state = fields.Selection(related='picking_id.state')

    move_line_ids = fields.One2many('stock.move.line', related='picking_id.move_line_ids')

    picking_type_code = fields.Selection(related='picking_id.picking_type_code')

    show_operations = fields.Boolean(related='picking_id.show_operations')
    show_reserved = fields.Boolean(related='picking_id.show_reserved')
    show_lots_text = fields.Boolean(related='picking_id.show_lots_text')
    has_tracking = fields.Boolean(related='picking_id.has_tracking')
    immediate_transfer = fields.Boolean(related='picking_id.immediate_transfer')
    sequence_code = fields.Char(related='picking_id.sequence_code')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("ref_id"):
                values['ref_id'] = f'default-{datetime.utcnow().timestamp()}'
        return super(ResPartner, self).create(vals_list)

    @api.model
    def create(self, vals):
        if not vals.get("ref_id"):
            vals['ref_id'] = f'default-{datetime.utcnow().timestamp()}'
        return super(ResPartner, self).create(vals)

    def booking_pos(self):
        picking_type = self.env['stock.picking.type'].search([('sequence_code', '=', 'BOOKING')], limit=1)
        view_id = self.env.ref('pos_machines.stock_picking_booking_form_view').id
        picking = self.env['stock.picking'].create({
            'partner_id': self.id,
            'picking_type_id': picking_type.id,
            'show_operations': True,
            'show_reserved': False,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id
        })

        self.write({'picking_id': picking.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Đặt máy làm hồ sơ',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': picking.id,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }

    # app rest api controller POS GET DELETE PUT => url /<db>/<model> api body
    def edit_booking(self):
        view_id = self.env.ref('stock.view_picking_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đặt máy làm hồ sơ',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.picking_id.id,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }

    def create_out_picking(self):

        for move_line in self.move_line_ids:

            if not move_line.account:
                raise UserError('Vui lòng cài đặt máy')

            if not move_line.account.ref_code:
                raise UserError('Vui lòng cài đặt máy')
        for return_move in self.picking_id.move_lines:
            return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

        for move_line in self.move_line_ids:
            move_line.account.send_backend()
        picking_type_id = self.env['stock.picking.type'].search([('sequence_code', '=', 'OUT')], limit=1)

        new_picking = self.picking_id.copy({
            'move_lines': [],
            'picking_type_id': picking_type_id.id,
            'state': 'assigned',
            'origin': f'Booking of {self.picking_id.name}',
            'location_id': self.picking_id.location_dest_id.id,
            'partner_id': self.id,
            'location_dest_id': self.property_stock_customer.id
        })

        new_picking.message_post_with_view('mail.message_origin_link',
                                           values={'self': new_picking, 'origin': self.picking_id},
                                           subtype_id=self.env.ref('mail.mt_note').id)
        self.write({
            'stock_out_picking_id': new_picking.id
        })

        new_picking.action_confirm()
        new_picking.action_assign()

        view_id = self.env.ref('pos_machines.stock_picking_booking_form_view').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Đặt máy làm hồ sơ',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': new_picking.id,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }
