import json, inspect
import logging
import traceback
import uuid
import sys
import tornado
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

__author__ = 'faisal'

"""
Server Usage:
server = Server(YourClass())
server.handle(request)

Client Usage: (Passing headers help with authorization cookies)
client = Client('http://path/to/rpc', headers)
client.method_name(args)
"""

VERSION = '2.0'
ERROR_MESSAGE = {
    -32700: 'Parse error',
    -32600: 'Invalid Request',
    -32601: 'Method not found',
    -32602: 'Invalid params',
    -32603: 'Internal error'
}


class ServerException(Exception):
    """
    code -32000 to -32099 for custom server errors
    """

    def __init__(self, data=None, message='Server error', code=-32000):
        Exception.__init__(self, message)
        self.data = data
        self.code = code
        self.message = message


class Server(object):
    response = None

    def __init__(self, obj):
        self.obj = obj

    def error(self, id, code, message='Server error', data=None):
        error_value = {'code': code, 'message': ERROR_MESSAGE.get(code, message)}
        if data:
            error_value['data'] = data
        return self.result({'jsonrpc': VERSION, 'error': error_value, 'id': id})

    def result(self, result):
        return result

    async def handle(self, request, data=None):
        if not data:
            try:
                data = tornado.escape.json_decode(request.body)
            except ValueError as e:
                return self.error(None, -32700)
        # batch calls
        if isinstance(data, list):
            batch_result = await gen.multi_future([self.handle(None, d) for d in data])
            return self.result(batch_result)

        if data.get('jsonrpc') != '2.0':
            return self.error(id, -32600)

        if 'id' in data:
            id = data['id']
        else:
            id = None

        if 'method' in data:
            method = data['method']
        else:
            return self.error(id, -32600)

        if 'params' in data:
            params = data['params']
        else:
            params = {}

        if method in vars(self.obj.__class__) and not method.startswith('_'):
            method = getattr(self.obj, method)
        else:
            return self.error(id, -32601)

        method_info = inspect.signature(method)
        arg_len = len(method_info.parameters)
        def_len = len(set(filter(lambda p: p.default is not inspect._empty,
                                 method_info.parameters.values())))

        # Check if params is valid and remove extra params
        named_params = not isinstance(params, list)
        invalid_params = False

        clean_params = {}
        if arg_len and params is None:
            invalid_params = True
        elif named_params:
            if arg_len:
                req_len = arg_len - def_len
                for i, arg in enumerate(method_info.parameters):
                    if arg in params:
                        clean_params[arg] = params[arg]
                    elif i <= req_len:
                        invalid_params = True
        else:
            if len(params) < arg_len - def_len:
                invalid_params = True

        if invalid_params:
            return self.error(id, -32602)
        try:
            if inspect.iscoroutinefunction(method):
                if named_params:
                    result = await method(**clean_params)
                else:
                    result = await method(*params)
            else:
                if named_params:
                    result = method(**clean_params)
                else:
                    result = method(*params)
                if type(result) is tornado.concurrent.Future:
                    result = await result
        except ServerException as e:
            return self.error(id, e.code, e.message, e.data)
        except:
            logging.error(sys.exc_info())
            traceback.print_exc()
            return self.error(id, -32603)

        if id is not None:
            return self.result({'result': result, 'id': id, 'jsonrpc': VERSION})


class Client(object):
    def __init__(self, uri, headers=None):
        self.uri = uri
        self.headers = headers or {}

    def __getattr__(self, method):

        def default(*args, **kwargs):
            params = {}
            if len(kwargs) > 0:
                params = kwargs
            elif len(args) > 0:
                params = args

            return self.request(method, params)

        return default

    async def request(self, method, params):
        parameters = {
            'id': str(uuid.uuid4()),
            'method': method,
            'params': params,
            'jsonrpc': VERSION
        }
        data = json.dumps(parameters)

        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.headers.items())
        req = HTTPRequest(self.uri, method='POST', headers=headers, body=data)
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(req)
        try:
            result = tornado.escape.json_decode(response.body)
        except:
            raise ServerException(ERROR_MESSAGE[-32700], code=-32700)

        if 'error' in result:
            raise ServerException(
                message='{} Code: {}'.format(result['error']['message'], result['error']['code']),
                code=result['error']['code']
            )
        elif parameters['id'] == result['id'] and 'result' in result:
            return result['result']
