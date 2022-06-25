
from logging import error
from sys import path_hooks
# from odoo import http
from odoo.http import request
import odoo.http as http

from datetime import datetime
from config import DefaultConfig

from botocore.exceptions import ClientError
from odoo import tools

# common header

class crosscheckingController(http.Controller):

    @http.route('/forcontrol', type='json',website=False, auth='public', methods=['POST'], csrf=False)
    def some_url(self, **arg):
        prod_obj = http.request.env['for.control'].one_more(arg)
        print('path in model ====', prod_obj)
        return {
            'name': 'TO MODEL C',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': prod_obj.get('url'),
        }



