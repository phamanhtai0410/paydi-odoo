# -*- coding: utf-8 -*-

# File: sock_move_line.py	
# Created at 29/11/2021

"""
   Description: 
        -
        -
"""
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = 'stock.move.line'

    account = fields.Many2one('account.pos.machines',
                              string='Tài khoản máy', readonly=True)
    is_setup = fields.Boolean(string="Cài máy")
    holder = fields.Many2one('res.partner', string='Giữ máy')

    @api.model
    def create(self, vals):
        pink = self.env['stock.picking'].search_read([('id', '=', vals.get('picking_id'))])

        vals['is_setup'] = False

        if pink and pink[0].get('name'):
            _name = pink[0].get('name').split('/')
            if len(_name) > 2 and _name[1] == 'OUT':
                vals['is_setup'] = True

        row = super(StockMoveLine, self).create(vals)
        return row

    @api.model
    def write(self, vals, *args, **kwargs):
        print('[debug] write', vals, args, kwargs)

        if vals.get('lot_id'):
            vals['account'] = None
        rows = super(StockMoveLine, self).write(vals)

        return rows

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.account and self.account.lot_id.id != self.lot_id.id:
            self.account = None

    def gen_account(self, *args, **kwargs):
        self.ensure_one()
        partner_id = self.picking_id.partner_id
        name = self.lot_id.name  # self.env['stock.production.lot'].search_read([('id', '=', default_lot_id)])

        # product_lot = value[0]
        # params = {
        #     'default_serial_number': name,
        #     'default_partner': partner_id.id,
        # }
        # view_id = self.env['pos.machine.setting.wizard']
        # new = view_id.create(params)
        # print('[debug] new', new)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cài đặt máy',
            'res_model': 'pos.machine.setting',
            'view_type': 'form',
            'view_mode': 'form',
            # 'res_id': new.id,
            # 'view_id': view_id,
            'target': 'new',
            'context': {
                'default_lot_id': self.lot_id.id,
                'default_partner': partner_id.id,
                'default_stock_move_line': self.id
            }
        }

    def account_get(self):
        print('account_get', self)
        if self.reference.split('/')[1] == 'OUT':
            return self.account
        return -1

    @api.model
    def _read_group_many2one_lot_id(self, records, domain, order):
        print('_read_group_many2one_lot_id', records, domain, order)
        return records
