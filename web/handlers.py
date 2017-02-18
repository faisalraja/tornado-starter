import logging
import mimetypes
import os
import time
from tornado import gen
from tornado.concurrent import run_on_executor
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    async def get(self):
        params = {}
        if self.get_arguments('test'):
            await gen.sleep(5)
        return self.render_template('main/index.html', **params)


class LoginHandler(BaseHandler):

    def get(self):

        return self.redirect(self.request.headers.get('Referer', '/'))


class LogoutHandler(BaseHandler):

    def get(self):

        return self.redirect(self.request.headers.get('Referer', '/'))
