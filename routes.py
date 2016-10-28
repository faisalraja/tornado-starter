from services import sample_jsonrpc
from web import admin, handlers

_routes = [
    # Main Routes
    (r'/', handlers.HomeHandler),
    (r'/admin', admin.HomeHandler),
    (r'/login', handlers.LoginHandler),
    (r'/logout', handlers.LoginHandler),
    (r'/rpc', sample_jsonrpc.ApiHandler)
]


def get_routes():
    return _routes
