# -*- coding: utf-8 -*-

# File: stock_move_line.py	
# Created at 29/11/2021

"""
   Description: 
        -
        -
"""
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    accounts = fields.One2many('account.pos.machines',
                               'lot_id',
                               string='Tài khoản máy')
