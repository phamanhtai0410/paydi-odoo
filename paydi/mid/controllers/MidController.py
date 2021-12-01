
from odoo import http
from odoo.http import request
import requests
import json

# common header
my_headers = {'api-key' : '1232', 'tenant': 'default'}
hostUrl = "http://localhost:81/mms"

class MidController(http.Controller):

    
    
    @http.route('/mid', type='http', auth="public", methods=['GET'], website=True)
    def getMid(self):
        mid = request.args.get('mid')
        responsePartner = requests.get("/mms/merchant/{mid}", headers=my_headers)
        partner = responsePartner.json()
        print(partner)
        return json.dumps(partner)
    
    
    
    
    @http.route('/mid', type='http', auth="public", methods=['POST'], website=True)
    def saveMid(self):
        
        responsePartner = requests.post(hostUrl + "/merchant", headers=my_headers)
        partner = responsePartner.json()
        print(partner)
        return json.dumps(partner)
    
    
    
    @http.route('/get-all-mid/<contactId>', type='http', auth="public", methods=['GET'], website=True)
    def getMidFromPartnerId(self,contactId):
       
        url = hostUrl + "/partner/contact/" + contactId
      
        responsePartner = requests.get(url, headers=my_headers)
        print("responsePartner", responsePartner.json())
        # partner = responsePartner.json().get('result').get('partner')
        merchants = responsePartner.json().get('result').get('listMerchant')

        
        print( "merchants", merchants)
        return http.request.render('mid.list-mid', {
            #'partner': partner,
            'merchants': merchants,
        })
    
    
    @http.route('/mid/create-template', type='http', auth="public", methods=['GET'], website=True)
    def getAddMidTemplate(self):
        
        url = hostUrl + "/merchant/template/"
        responseMerchantTemplate = requests.get(url, headers=my_headers)
        merchantTemplate = responseMerchantTemplate.json().get('result')
        print("merchantCode", merchantTemplate.get('listMerchantCode'))
      
        return http.request.render('mid.add-mid', {
            'merchantTemplate': merchantTemplate,
            'merchantCode': merchantTemplate.get('listMerchantCode')
        })
        
