from odoo import fields, models, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    odoo_contact_id = fields.One2many(comodel_name="fee.installment", string="odoo contact id",inverse_name="merchant_id")

    def get_fee_installment(self, arg):
        _merchant_id = int(arg.get('odoo_contact_id'))
        fee_by_merchant = self.env["fee.installment"].search_read([("merchant_id","=",_merchant_id)])
        return fee_by_merchant