# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, tools
from odoo.http import request,route,Controller
from ..models import vietqr
import werkzeug.exceptions
import logging
_log = logging.getLogger(__name__)
class BeanController(Controller):
#     @http.route('/first-module/first-module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/first-module/first-module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('first-module.listing', {
#             'root': '/first-module/first-module',
#             'objects': http.request.env['first-module.first-module'].search([]),
#         })

#     @http.route('/first-module/first-module/objects/<model("first-module.first-module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('first-module.object', {
#             'object': obj
#         })

    @route(['/vietqr','/vietqr/<path:value>', '/vietqr/<bill_value>/<bill_purpose>/<path:value>'], type='http', auth="public",cors="*")
    def get_vietqr(self,bill_value='',bill_purpose='', bill_no='', **kwargs):
        """Contoller able to render VietQR images 
        Samples::

            <img t-att-src="'/vietqr/20000/%s' % ('Thanh toan mua hang')"/>
            <img t-att-src="'/vietqr?bill_value=%s&amp;bill_purpose=%s&amp;width=%s&amp;height=%s' %
                (20000, 'Thanh toan bill', 200, 200)"/>

        :param bill_value: Value of the bill
        :param bill_purpose: Payment purpose
        :param width: Pixel width of the barcode
        :param height: Pixel height of the barcode
        :param humanreadable: Accepted values: 0 (default) or 1. 1 will insert the readable value
        at the bottom of the output image
        :param quiet: Accepted values: 0 (default) or 1. 1 will display white
        margins on left and right.
        :param mask: The mask code to be used when rendering this QR-code.
                     Masks allow adding elements on top of the generated image,
                     such as the Swiss cross in the center of QR-bill codes.
        :param barLevel: QR code Error Correction Levels. Default is 'L'.
        ref: https://hg.reportlab.com/hg-public/reportlab/file/830157489e00/src/reportlab/graphics/barcode/qr.py#l101
        """
        try:
            #Check Variables
            if kwargs.get('acc_no') is not None:
                acc_no = kwargs.get('acc_no')
                is_bank_acc = True if acc_no.find("9704") else False
            else:
                acc_no = '129005718'
                is_bank_acc = True
                
            _log.debug("\nbank acc: %s \n" % (kwargs.get('bank_acc')))
            if kwargs.get('bank_acc') == False or kwargs.get('bank_acc') is None or len(str(kwargs.get('bank_acc')).split(","))==1:    
                acc_name = kwargs.get('acc_name') if kwargs.get('acc_name') is not None else 'NGUYEN PHAM THUY LAN'
                acc_bic = kwargs.get('bank_code') if kwargs.get('bank_code') is not None else '970432'
            else:
                ba = str(kwargs.get('bank_acc')).split(",")
                _log.debug("\nbank_acc --- %s -- %s \n" % (ba, len(ba)))
                ba = ba[1].split("-")
                acc_name = ba[2]
                acc_bic = ba[1]
                acc_no = ba[0]
            
            qr_height = kwargs.get('height') if kwargs.get('height') is not None else 120
            qr_weight = kwargs.get('weight') if kwargs.get('weight') is not None else 120
            
            qrtype = False if (kwargs.get('qrtype')== 'static' and kwargs.get('qrtype') is not None) else True
            #remove all , and . out of billvalue
            bill_value = bill_value.replace(".","").replace(",","")
            
            #Generate VietQR value
            value = vietqr.gen_vietqr_string(bill_value=bill_value,bill_no= bill_no,bill_detail=bill_purpose,acc_no=acc_no,acc_holder_name=acc_name, acc_bic=acc_bic,qrtype=qrtype,is_bank_acc=is_bank_acc)
            _log.debug ("\n %s" % value)
            
            qrcode = request.env['ir.actions.report'].barcode("QR", value,width=qr_weight, height=qr_height)
        except (ValueError, AttributeError):
            raise werkzeug.exceptions.HTTPException(description='Cannot convert into barcode.')

        return request.make_response(qrcode, headers=[('Content-Type', 'image/png')])
         
