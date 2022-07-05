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


    def _get_stock_picking_ids_draft(self):
        for record in self:
            stock_picking_ids_draft = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    if x.picking_id.state == "draft" :
                        stock_picking_ids_draft.append(x.picking_id.id)
            record.update({'stock_picking_ids_draft': [(6, 0, stock_picking_ids_draft or [])]})

    stock_picking_ids_draft = fields.One2many('stock.picking', compute='_get_stock_picking_ids_draft')

    def _get_stock_picking_ids_ready(self):
        for record in self:
            stock_picking_ids_ready = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    if x.picking_id.state == "assigned" :
                        stock_picking_ids_ready.append(x.picking_id.id)
            record.update({'stock_picking_ids_ready': [(6, 0, stock_picking_ids_ready or [])]})

    stock_picking_ids_ready = fields.One2many('stock.picking', compute='_get_stock_picking_ids_ready')
    
    def _get_stock_picking_ids_done(self):
        for record in self:
            stock_picking_ids_done = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    if x.picking_id.out_picking_id == False and x.picking_id.return_picking_id != False or x.picking_id.out_picking_id_state != "done" and x.picking_id.show_booking == False and  x.picking_id.state == "done" :
                        stock_picking_ids_done.append(x.picking_id.id)
            record.update({'stock_picking_ids_done': [(6, 0, stock_picking_ids_done or [])]})

    stock_picking_ids_done = fields.One2many('stock.picking', compute='_get_stock_picking_ids_done')

    def _get_stock_picking_ids_donereturn(self):
        for record in self:
            stock_picking_ids_donereturn = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    if x.picking_id.out_picking_id == False and x.picking_id.return_picking_id != False or x.picking_id.out_picking_id_state == "done" and x.picking_id.show_booking == False:
                        stock_picking_ids_donereturn.append(x.picking_id.id)
            record.update({'stock_picking_ids_donereturn': [(6, 0, stock_picking_ids_donereturn or [])]})

    stock_picking_ids_donereturn = fields.One2many('stock.picking', compute='_get_stock_picking_ids_donereturn')

    def _get_stock_picking_ids_cancel(self):
        for record in self:
            stock_picking_ids_cancel = []
            if record.stock_book_lines:
                for x in record.stock_book_lines:
                    if x.picking_id.state == "cancel" :
                        stock_picking_ids_cancel.append(x.picking_id.id)
            record.update({'stock_picking_ids_cancel': [(6, 0, stock_picking_ids_cancel or [])]})

    stock_picking_ids_cancel = fields.One2many('stock.picking', compute='_get_stock_picking_ids_cancel')

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
    
    is_approved_user_id = fields.Boolean(default=False, compute='_get_current_user_details')    

    def _get_current_user_details(self):
        current_user = self.env['res.users'].search([('id','=',self.env.user.id)]) 
        _company_id = current_user.company_id.id
        if _company_id == 2:
            self.is_approved_user_id = False
        else:
            self.is_approved_user_id = True
        