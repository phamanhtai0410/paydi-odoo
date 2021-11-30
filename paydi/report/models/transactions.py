# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ReportTransactions(models.Model):
    _name = 'report.transactions'
    _description = 'Detail of Transactions'

    tid = fields.Char(string="Mã TID", required=True)
    mid = fields.Char(string="Mã MID", required=True)
    pos_id = fields.Char(string="ID máy POS", required=True)
    amount = fields.Integer(string="Giá trị giao dịch", required=True)
    transaction_err = fields.Char("Mã lỗi giao dịch (nếu có)", required=True)
    
