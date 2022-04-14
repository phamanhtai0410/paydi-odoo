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
        for record in self:
            record.ref_view = ''
            if record.ref_id and 'default-' not in record.ref_id:
                record.ref_view = record.ref_id

    def _set_ref_view(self):
        for record in self:
            if record.ref_view:
                record.ref_id = record.ref_view

    ref_view = fields.Char(compute='_get_ref_view', inverse='_set_ref_view')
    stock_book_lines = fields.One2many('stock.book.line', 'partner_id')

    def _get_stock_picking_ids_draf(self):
        for record in self:
            stock_picking_ids_draf = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    stock_picking_ids_draf.append(x.picking_id.id)
            record.update({'stock_picking_ids_draf': [(6, 0, stock_picking_ids_draf or [])]})

            res_draf = {}
            res_draf['domain'] = {'stock_picking_ids_done': [('state', '!=', 'draf')]}
            return res_draf
    def _get_stock_picking_ids_ready(self):
        for record in self:
            stock_picking_ids_ready = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    stock_picking_ids_ready.append(x.picking_id.id)
            record.update({'stock_picking_ids_ready': [(6, 0, stock_picking_ids_ready or [])]})

            res_ready = {}
            res_ready['domain'] = {'stock_picking_ids_done': [('state', '!=', 'ready')]}
            return res_ready

    def _get_stock_picking_ids_done(self):
        for record in self:
            stock_picking_ids_done = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    stock_picking_ids_done.append(x.picking_id.id)
            record.update({'stock_picking_ids_done': [(6, 0, stock_picking_ids_done or [])]})

            res_done = {}
            res_done['domain'] = {'stock_picking_ids_done': [('state', '!=', 'done')]}
            return res_done

    def _get_stock_picking_ids_return(self):
        for record in self:
            stock_picking_ids_return = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    stock_picking_ids_return.append(x.picking_id.id)
            record.update({'stock_picking_ids_return': [(6, 0, stock_picking_ids_return or [])]})

            res_return = {}
            res_return['domain'] = {'stock_picking_ids_done': [('return_picking_id', '!=',False), ('out_picking_id', '=', False),( 'out_picking_id_state', '!=', 'done'), ('show_booking','=', False)]}
            return res_return

    stock_picking_ids_draf = fields.One2many('stock.picking', compute='_get_stock_picking_ids_draf')

    stock_picking_ids_ready = fields.One2many('stock.picking', compute='_get_stock_picking_ids_ready')

    stock_picking_ids_done = fields.One2many('stock.picking', compute='_get_stock_picking_ids_done')

    stock_picking_ids_return = fields.One2many('stock.picking', compute='_get_stock_picking_ids_return')

    account_ids = fields.One2many('account.pos.machines', 'partner_id', domain=[('status', '!=', 'return_machine')])

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

        self.env['stock.book.line'].create({
            'partner_id': self.id,
            'picking_id': picking.id
        })

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

    def create_out_picking(self):

        for move_line in self.move_line_ids:

            if not move_line.account:
                raise UserError('Vui lòng cài đặt máy')

            if not move_line.account.ref_codes:
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
