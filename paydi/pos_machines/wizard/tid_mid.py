# -*- coding: utf-8 -*-

# File: tid_mid.py
# Created at 30/11/2021

"""
   Description: 
        -
        -
"""
from odoo import fields, models, api


class PosMachineTIDMID(models.TransientModel):
    _name = 'pos.machine.tid.mid.wizard'

    pos_setting = fields.Many2one('pos.machine.setting.wizard', string='Máy')
    acq_code = fields.Char(string="ACQ")
    tid = fields.Char(string="Mã TID")
    mid = fields.Char(string="Mã MID")
