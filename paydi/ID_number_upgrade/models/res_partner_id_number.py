
from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _name = "res.partner.id_number"
    _inherit = "res.partner.id_number"

    position = fields.Char(
        string="Chức vụ",
    )
    Representative_information = fields.Char(
        string="Thông tin người đại diện",
        help="The place where the ID has been issued. For example the country "
        "for passports and visa",
    )
    contract_payment_date = fields.Date(
        string="Ngày trả hợp đồng cho đơn vị",
    )