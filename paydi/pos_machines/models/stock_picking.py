from copy import copy, deepcopy
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # partner_id = fields.Many2one('res.partner', string='Hồ sơ đăng ký')
    sequence_code = fields.Char(related="picking_type_id.sequence_code")

    return_from_picking_id = fields.Many2one('stock.picking')

    def _get_return_picking_id(self):
        for record in self:
            record.return_picking_id = False
            if record.out_picking_id and not record.return_from_picking_id:
                return_picking_id = self.env['stock.picking'].search([('return_from_picking_id', '=', record.id)],
                                                                     limit=1)
                print('return_picking_id', return_picking_id)
                if return_picking_id:
                    record.return_picking_id = return_picking_id

    out_picking_id = fields.Many2one('stock.picking')
    return_picking_id = fields.Many2one('stock.picking', compute='_get_return_picking_id')
    out_picking_id_state = fields.Selection(related='out_picking_id.state')

    def _get_first_stock_production_lot(self):
        for record in self:
            record.first_stock_production_lot = False
            if len(record.move_line_ids) > 0:
                record.first_stock_production_lot = record.move_line_ids[0].lot_id

    first_stock_production_lot = fields.Many2one('stock.production.lot', compute='_get_first_stock_production_lot')

    def _get_show_booking(self):
        show_booking = self.env.context.get('show_booking') or False
        for record in self:
            record.show_booking = show_booking

    show_booking = fields.Boolean(compute='_get_show_booking')

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
        if len(self.move_line_ids_without_package) > 1 and self.sequence_code == 'BOOKING':
            raise ValidationError('Tối đa 1 máy')

    def make_return(self):
        for line in self.move_line_ids:
            if line.account.status == 'active':
                raise ValidationError(f'Vui lòng khóa tài khoản {line.account.username}, trước khi hoàn trả máy')
        for line in self.move_line_ids:
            line.account.write({
                'status': 'return_machine'
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reverse Transfer',
            'res_model': 'stock.return.picking',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.out_picking_id.id,
                'active_model': 'stock.picking',
                'default_return_from_picking_id': self.id
            }
        }

    def act_stock_booking_picking_config(self):
      
        picking_type_id = self.env['stock.picking.type'].search([('sequence_code', '=', 'OUT')], limit=1)
        new_picking = {
            
            'origin': f'Booking of {self.name}',
            'move_type' : 'direct',
            'state': 'draft',
            'scheduled_date': self.scheduled_date,
            'has_deadline_issue': False,
            'location_id': self.location_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'picking_type_id': picking_type_id.id,
            'company_id': self.company_id.id,
            'user_id': self.user_id.id,
            'is_locked': False,
            'partner_id': self.partner_id.id,
        }
        
        result = self.env['stock.picking'].browse(self.id).copy({
            'state': 'draft',
            'is_locked': False,
            'origin': f'Booking of {self.name}',
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'picking_type_id': picking_type_id.id,
            # 'move_line_ids': [(4,move_line_new.id)]
        })

        move_line_ids = self.move_line_ids[0]
        move_line_new = move_line_ids.copy({
            'picking_id': result.id,
            'reference':result.name,
        })

        self.write({
            'out_picking_id' : result.id
        })


    def act_return_stock_booking_picking(self):
        picking_name = self.name
        print('picking name ======================', picking_name)
        if picking_name.find("ATOM") != -1:
            picking_type_id = self.env['stock.picking.type'].search([('sequence_code', '=', 'A-RETURN')], limit=1)
            print('pciking type id ========================', picking_type_id)
        if picking_name.find('PD-DN') != -1:
            picking_type_id = self.env['stock.picking.type'].search([('sequence_code', '=', 'P-RETURN')], limit=1)
        # picking_type_id = self.env['stock.picking.type'].search([('sequence_code', '=', 'A-RETURN')], limit=1)

        result = self.env['stock.picking'].browse(self.id).copy({
            'state': 'draft',
            'is_locked': False,
            'origin': f'Return of {self.name}',
            'location_id': self.partner_id.property_stock_customer.id,
            'location_dest_id': self.location_id.id,
            'picking_type_id': picking_type_id.id,
            'out_picking_id' : '',
        })

        move_line_ids = self.move_line_ids[0]
        move_line_new = move_line_ids.copy({
            'picking_id': result.id,
            'reference':result.name,
        })

        self.write({
            'return_from_picking_id' : result.id,
            'is_locked': True,
            'state': 'done'
        })

