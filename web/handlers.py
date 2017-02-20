import logging
import mimetypes
import os
import time
import uuid
from authomatic import Authomatic
from lib.auth_adapter import TornadoWebAdapter
from tornado import gen
import config
from lib.basehandler import BaseHandler
from models import models


authomatic = Authomatic(config=config.auth, secret=config.cookie_secret, debug=config.is_local)


class HomeHandler(BaseHandler):

    async def get(self):
        params = {}
        if self.get_argument('test', None):
            await self.run_async(time.sleep, 3)
        return self.render_template('main/index.html', **params)


class LoginHandler(BaseHandler):

    @classmethod
    def login_or_create(cls):
        user = models.User.get_user_by_login('A@A.A', '1')

        if not user:
            user = models.User.register(name='Test User', email='A@A.A', password='1')
            user.save()

        return user

    @gen.coroutine
    def get(self):

        user = yield self.run_async(self.login_or_create)
        self.set_secure_cookie('user_id', str(user.id))

        return self.redirect(self.request.headers.get('Referer', '/'))


class LoginProviderHandler(BaseHandler):

    def on_login(self, result):
        if result:
            if result.error:
                logging.error('Error: {}'.format(result.error))
                return self.redirect('/')
            elif result.user:
                if not (result.user.name and result.user.id):
                    result.user.update()
                logging.info('User: {}'.format(result.user))
                user = models.User.get_user_by_oauth(result)
                if user:
                    self.set_secure_cookie('user_id', str(user.id))
                return self.redirect('/')

    def handle(self, provider):
        authomatic.login(TornadoWebAdapter(self), provider, self.on_login)

    @gen.coroutine
    def get(self, provider):
        yield self.run_async(self.handle, provider)

    @gen.coroutine
    def post(self, provider):
        yield self.run_async(self.handle, provider)


class LogoutHandler(BaseHandler):

    def get(self):

        self.clear_cookie('user_id')

        return self.redirect(self.request.headers.get('Referer', '/'))
