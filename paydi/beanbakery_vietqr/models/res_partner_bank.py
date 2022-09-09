from odoo import models, fields, api, _
from . import vietqr

""" Customize the res_partner_bank model
    - Add @static_qr to store the Napas static account QR string
    - Add compute function for @acc_holder_name to get partner name when the @partner_id is change
    - Add compute function for @currency_id to get the default currency_id of current Company
    - Customize the name_get function to show bank account name as 'acc_number-acc_bank_name-acc_holder_name'
"""

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"
    
    
    static_qr = fields.Char ("Static QR", compute="_make_static_qr",store=True)
    acc_holder_name = fields.Char(string='Account Holder Name', help="Account holder name, in case it is different than the name of the Account Holder",
                                    store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    def name_get(self):
        res = []
        for item in self:
            name = "%s-%s-%s" % (item.acc_number,item.bank_id.name,item.acc_holder_name if (item.acc_holder_name!=False) else "No name")
            res.append((item.id,name))
           
        return res
    
    @api.depends('acc_number','bank_bic')
    def _make_static_qr(self):
        for acc in self:
            is_bank_acc = True
            if acc.acc_number != False and "9704" in acc.acc_number:
                is_bank_acc = False
            print("is_bank_acc ---- ",is_bank_acc)
            acc.static_qr = vietqr.gen_vietqr_url(acc_no = str(acc.acc_number),acc_holder_name=str(acc.acc_holder_name),
                                    acc_bic=str(acc.bank_bic),qrtype=False,is_bank_acc=is_bank_acc)
            
    @api.depends('partner_id')
    def _add_partner_name(self):
        print("self.env.company.currency_id",self.env.company.currency_id)
        for acc in self:
            if acc.partner_id != False:
                acc.acc_holder_name = acc.partner_id.name
            
    """_This section is Override the original 'retrieve_acc_type' function_
        Logic:
            - Check if '9704' is exist in acc_number , that is an ATM card account
            - Otherwise, that is a bank account
    """
    @api.model
    def retrieve_acc_type(self, acc_number):
        """ To be overridden by subclasses in order to support other account_types.
        """
        if  acc_number == False or "9704" not in acc_number:
            return 'bank'
        else:
            return 'atm'
        
    """_This section is Override the original '_get_supported_account_types' function_
       -  The original Odoo only support 'bank' type
       -  We add more custome bank type or e-wallet account type here
    """
    @api.model
    def _get_supported_account_types(self):
        return [('bank', _('Bank account')),
                ('atm', _('ATM card'))]
            
        