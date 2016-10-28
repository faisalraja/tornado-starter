import logging
import mimetypes
import os
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        params = {}
        return self.render_template('main/index.html', **params)


class LoginHandler(BaseHandler):

    def get(self):

        return self.redirect(self.request.headers.get('Referer', '/'))


class LogoutHandler(BaseHandler):

    def get(self):

        return self.redirect(self.request.headers.get('Referer', '/'))
