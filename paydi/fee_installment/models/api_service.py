from odoo import fields, models, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    odoo_contact_id = fields.One2many(comodel_name="fee.installment", string="odoo contact id",inverse_name="merchant_id")

    def get_fee_installment(self, arg):
        _merchant_id = int(arg.get('odoo_contact_id'))
        fee_by_merchant = self.env["fee.installment"].sudo().search([("merchant_id","=",_merchant_id)])
        result = []
      
        for rec in fee_by_merchant:
            result.append({
                
                "name": rec['bank']['name'],
                "bank_code":rec['bank']['code'],
                "period" : rec['period'],
                "fee_installment" : rec['fee_installment'],
                "from_date" : rec['from_date'],
                "to_date" : rec['to_date']
            })
        
        return result