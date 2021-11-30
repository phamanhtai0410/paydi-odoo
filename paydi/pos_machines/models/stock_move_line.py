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
                              string='Tài khoản máy')
    is_setup = fields.Boolean(string="Cài máy")

    @api.model
    def create(self, vals):
        pink = self.env['stock.picking'].search_read([('id', '=', vals.get('picking_id'))])
        if pink and pink[0].get('name').split('/')[1] == 'OUT':
            vals['is_setup'] = True
        else:
            vals['is_setup'] = False
        rows = super(StockMoveLine, self).create(vals)

        return rows

    def gen_account(self, *args, **kwargs):
        self.ensure_one()
        partner_id = self.picking_id.partner_id
        name = self.lot_id.name  # self.env['stock.production.lot'].search_read([('id', '=', default_lot_id)])

        print('[debug] self.picking_id', self, name)
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
            print('heeeeeeeee')
            return self.account
        print('-111111111111')
        return -1
