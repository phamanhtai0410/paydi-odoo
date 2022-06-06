
from logging import error
from sys import path_hooks
# from odoo import http
from odoo.http import request
import odoo.http as http
import requests
import json
from datetime import datetime
from config import DefaultConfig
import boto3
import uuid
from botocore.exceptions import ClientError
from odoo import tools
import re
import hashlib
import hmac
# common header

class exportController(http.Controller):

    @http.route('/exportfee', type='json',website=False, auth='public', methods=['POST'], csrf=False)
    def some_url(self, **arg):
        print("=============================================================")
        print(arg)
        print("=============================================================")

        prod_obj = http.request.env['res.partner'].export_action_withdate(arg)


