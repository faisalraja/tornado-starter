from tornado.web import url
from services import rpc
from web import admin, handlers

_routes = [
    # Main Routes
    (r'/', handlers.HomeHandler),
    (r'/admin', admin.HomeHandler),
    (r'/login', handlers.LoginHandler),
    url(r'/login/(google|twitter)', handlers.LoginProviderHandler, name='login-provider'),
    (r'/logout', handlers.LogoutHandler),
    (r'/rpc', rpc.ApiHandler)
]


def get_routes():
    return _routes
