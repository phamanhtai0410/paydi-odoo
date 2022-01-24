# -*- coding: utf-8 -*-

# File: res_partner.py
# Created at 07/12/2021

"""
   Description:
        -
        -
"""
import json
import traceback
from datetime import datetime
import math

import odoo.exceptions
from odoo import http, _, exceptions
from odoo.http import Response
from odoo.http import request
from .exceptions import QueryFormatError
from .serializers import Serializer

_prefix = '/api/v1/'


def make_response(data: dict = {}, msg: str = '', error=None, status=1, error_code=0):
    return {
        "version": "1.0",
        "error": {
            "name": str(error),
            "message": msg,
            "arguments": list(error.args),
            "exception_type": type(error).__name__
        } if error else {},
        'time': datetime.utcnow().timestamp(),
        'data': data,
        'msg': msg,
        'status': status,
        'error_code': error_code
    }


class HandlerController(http.Controller):
    @http.route(
        f'{_prefix}login/',
        type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **kwargs):
        print('authenticate', kwargs)
        try:
            login = kwargs["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')

        try:
            password = kwargs["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')
        #
        # try:
        #     db = kwargs["db"]
        # except KeyError:
        #     raise exceptions.AccessDenied(message='`db` is required.')
        try:
            http.request.session.authenticate('paydi', login, password)

            res = request.env['ir.http'].session_info()
            res = make_response(data=res)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )
        except odoo.exceptions.AccessDenied:
            traceback.print_exc()
            res_error = make_response(msg='AccessDenied', error=None, status=0, error_code=403)
            return http.Response(
                json.dumps(res_error),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            traceback.print_exc()
            res_error = make_response(msg='Exception', error=e, status=0, error_code=500)
            return http.Response(
                json.dumps(res_error),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        f'{_prefix}object/<string:model>/<string:function>',
        type='json', auth='user', methods=["POST"], csrf=False)
    def call_model_function(self, model, function, **post):
        args = []
        kwargs = {}
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]
        model = request.env[model]
        result = getattr(model, function)(*args, **kwargs)
        return result

    @http.route(
        f'{_prefix}object/<string:model>/<int:rec_id>/<string:function>',
        type='json', auth='user', methods=["POST"], csrf=False)
    def call_obj_function(self, model, rec_id, function, **post):
        args = []
        kwargs = {}
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]
        obj = request.env[model].browse(rec_id).ensure_one()
        result = getattr(obj, function)(*args, **kwargs)
        return result

    @http.route(
        f'{_prefix}/object/<string:model>',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_model_data(self, model, **params):
        print('get_model_data______get_model_data', http.request.params)
        limit = params.get('limit', 20)
        offset = params.get('offset', 0)

        if "query" in params:
            query = params["query"]
        else:
            query = "{*}"

        if "order" in params:
            orders = json.loads(params["order"])
        else:
            orders = ""
        try:
            print('filter', params)
            if "filter" in params:
                filters = json.loads(params["filter"])
                records = request.env[model].search(filters, order=orders, limit=limit, offset=offset)
            else:
                records = request.env[model].search([])
        except KeyError as e:
            msg = "The model `%s` does not exist." % model
            res = make_response(error=e, msg=msg, status=0, error_code=404)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )
        try:
            serializer = Serializer(records, query, many=True)
            data = serializer.data
        except (SyntaxError, QueryFormatError) as e:
            res = make_response(error=e, msg=e.msg, status=0, error_code=401)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )
        res = make_response(data={
            'value': data
        })

        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )

    @http.route(
        f'{_prefix}<string:model>/',
        type='json', auth="user", methods=['POST'], csrf=False)
    def post_model_data(self, model, **post):
        try:
            data = post['data']
        except KeyError:
            msg = "`data` parameter is not found on POST request body"
            raise exceptions.ValidationError(msg)

        try:
            model_to_post = request.env[model]
        except KeyError:
            msg = "The model `%s` does not exist." % model
            raise exceptions.ValidationError(msg)

        # TODO: Handle data validation

        if "context" in post:
            context = post["context"]
            record = model_to_post.with_context(**context).create(data)
        else:
            record = model_to_post.create(data)
        return record.id

    # bulk
    @http.route(
        f'{_prefix}<string:model>/',
        type='json', auth="user", methods=['PUT'], csrf=False)
    def put_model_records(self, model, **kwargs):
        try:
            data = kwargs['data']
        except KeyError:
            msg = "`data` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)

        try:
            model_to_put = request.env[model]
        except KeyError:
            msg = "The model `%s` does not exist." % model
            raise exceptions.ValidationError(msg)

        # TODO: Handle errors on filter
        filters = kwargs["filter"]

        if "context" in kwargs:
            recs = model_to_put.with_context(**kwargs["context"]) \
                .search(filters)
        else:
            recs = model_to_put.search(filters)

        # TODO: Handle data validation
        for field in data:
            if isinstance(data[field], dict):
                operations = []
                for operation in data[field]:
                    if operation == "push":
                        operations.extend(
                            (4, rec_id, _)
                            for rec_id
                            in data[field].get("push")
                        )
                    elif operation == "pop":
                        operations.extend(
                            (3, rec_id, _)
                            for rec_id
                            in data[field].get("pop")
                        )
                    elif operation == "delete":
                        operations.extend(
                            (2, rec_id, _)
                            for rec_id in
                            data[field].get("delete")
                        )
                    else:
                        pass  # Invalid operation

                data[field] = operations
            elif isinstance(data[field], list):
                data[field] = [(6, _, data[field])]  # Replace operation
            else:
                pass

        if recs.exists():
            try:
                return recs.write(data)
            except Exception as e:
                # TODO: Return error message(e.msg) on a response
                return False
        else:
            # No records to update
            return True
