# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from typing_extensions import Required
from odoo import models, fields


class Transactions(models.Model):
    _name = 'report.transactions'
    _description = 'Detail of Transactions'

    tid = fields.Char(string="Mã TID", tracking=True)
    mid = fields.Char(string="Mã MID", tracking=True)
    pos_id = fields.Char(string="ID máy POS", tracking=True)
    amount = fields.Integer(string="Giá trị giao dịch", tracking=True)
    transaction_err = fields.Char("Mã lỗi giao dịch (nếu có)", tracking=True)
    
