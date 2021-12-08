# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ReportTransactions(models.Model):
    _name = 'report.transactions'
    _description = 'Detail of Transactions'

    account_id = fields.Char(string="ID của tài khoản", required=True)
    created_time = fields.Datetime(string="Ngày tạo giao dịch", required=True)
    error_msg = fields.Char(string="Mã lỗi gia dịch (nếu có)", required=True)
    merchant_id = fields.Char(string="ID của merchant", required=True)
    obj_type = fields.Char(string="Loại thanh toán", required=True)
    pos_id = fields.Char(string="ID của máy POS", required=True)
    tid = fields.Char(string="Mã TID", required=True)
    total_amount = fields.Integer(string="Giá trị giao dịch", required=True)
    
    card_type = fields.Char(string="Loại thẻ")


    # app_ver = fields.Char(string="Phiên bản của app")
    # approve_code = fields.Char(string="Mã code để duyệt")
    # bank_merchant_id = fields.Char(string="Mã ID của ngân hàng")
    # batch_no = fields.Char(string="Mã lô")
    # card_holder = fields.Char(string="Tên trên thẻ")
    # card_number = fields.Char(string="Số thẻ")   
    # code = fields.Integer(string="Mã code kq giao dịch")  
    # currency = fields.Char(string="Đơn vị tiền tệ")
    # desc = fields.Char(string="Kết quả giao dịch")
    # exp_date = fields.Char(string="Ngày hết hạn")
    # invoice_no = fields.Char(string="Mã hóa đơn")
    # iso_response_code = fields.Char(string="Mã trả từ ngân hàng")
    # merchant_trans_id = fields.Char(string="Mã giao dịch của ngân hàng")
    # ref_no = fields.Char(string="Mã ref")
    # req_acqr_id = fields.Char(string="Số thẻ")
    # req_card_type = fields.Char(string="Số thẻ")
    # req_currency_name = fields.Char(string="Số thẻ")
    # req_merchant_trans_id = fields.Char(string="Số thẻ")
    # req_tip_amount = fields.Char(string="Số thẻ")
    # req_transaction_amount = fields.Char(string="Số thẻ")
    # req_tranx_type = fields.Char(string="Số thẻ")
    # status = fields.Char(string="Số thẻ")
    # swipe_type = fields.Char(string="Số thẻ")
    # terminal_id = fields.Char(string="Số thẻ")
    # trace_no = fields.Char(string="Số thẻ")
    # trans_date_time = fields.Char(string="Số thẻ")
    # tranx_type = fields.Char(string="Số thẻ")
    # has_voided = fields.Char(string="Số thẻ")
    # void_data = fields.Char(string="Số thẻ")

          


    
