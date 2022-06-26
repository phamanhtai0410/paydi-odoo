

from odoo import _, api, models , fields
from odoo.exceptions import ValidationError

class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"
    _description = "Partner ID Number"
    _order = "name"
    
    position = fields.Char(
        string="Chức vụ",
    )
    Representative_information = fields.Char(
        string="Thông tin người đại diện",
    )
    contract_payment_date = fields.Date(
        string="Ngày trả hợp đồng cho đơn vị",
    )
