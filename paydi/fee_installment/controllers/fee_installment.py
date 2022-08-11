import odoo.http as http

class FeeInstallmentController(http.Controller):

    @http.route('/get-fee-installment', type='json',website=False, auth='public', methods=['POST'], csrf=False, cors="*")
    def get_fee(self, **arg):
        # print('------------------self----------------------', self)
        # flag = http.request.jsonrequest
        # print('============flag=======', flag)
        result = http.request.env['res.partner'].get_fee_installment(arg)
        if result:    
            data = {
                'fee_installment' : result
            }
            return data
        else:
            return 'fee_installment_not_found'
