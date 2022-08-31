from odoo import fields, models, api
from dateutil import tz
import datetime
import pytz


class TransactionInstallment(models.Model):
    _name = "transaction.installment"
    _description = "Description"
    _order = "date_trans desc"

    date_trans = fields.Float(string="date_trans")
    bank = fields.Char(string="Ngân hàng")
    card_organization = fields.Char(string="Loại thẻ")
    name_card = fields.Char(string="Họ và tên chủ thẻ")
    card_number = fields.Char(string="Số thẻ của chủ thẻ")
    total_amount = fields.Float(string="Số tiền đăng ký trả góp")
    period = fields.Integer(string="Kỳ hạn")
    identity_card = fields.Char(string="Giấy tờ tùy thân")
    approve_code = fields.Char(string="Approval code")
    phone = fields.Char(string="Số điện thoại")
    date_display = fields.Char("Ngày bắt đầu")
    contact_id = fields.Many2one(comodel_name="res.partner", string="Tên Merchant", required="1")

    def make_order(self):
        return ""

    def convert_uct_to_asia(sefl, date_time):

        from_zone = tz.gettz("UTC")
        to_zone = tz.gettz("Asia/Ho_Chi_Minh")
        utc = datetime.datetime.strptime(date_time, "%d/%m/%YT%H:%M:%S")
        utc = utc.replace(tzinfo=from_zone)
        _central = utc.astimezone(to_zone)
        central = _central.strftime("%d-%m-%Y %H:%M:%S")

        return central

    def convert_asia_to_uct(self, date_time):
        local = pytz.timezone("Asia/Ho_Chi_Minh")
        naive = datetime.datetime.strptime(date_time, "%d-%m-%Y %H:%M:%S")
        local_dt = local.localize(naive, is_dst=None)
        _utc_dt = local_dt.astimezone(pytz.utc)
        utc_dt = _utc_dt.strftime("%d/%m/%YT%H:%M:%S")
        return utc_dt
