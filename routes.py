from services import rpc
from web import admin, handlers

_routes = [
    # Main Routes
    (r'/', handlers.HomeHandler),
    (r'/admin', admin.HomeHandler),
    (r'/login', handlers.LoginHandler),
    (r'/logout', handlers.LoginHandler),
    (r'/rpc', rpc.ApiHandler)
]


def get_routes():
    return _routes
