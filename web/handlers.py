import logging
import mimetypes
import os
import time
import uuid
from authomatic import Authomatic
from lib.auth_adapter import TornadoWebAdapter
from tornado import gen
from tornado.concurrent import run_on_executor
import config
from lib.basehandler import BaseHandler
from models import models


authomatic = Authomatic(config=config.auth, secret=str(uuid.uuid4()), debug=config.is_local)


class HomeHandler(BaseHandler):

    async def get(self):
        params = {}
        if self.get_argument('test', None):
            await gen.sleep(5)
        return self.render_template('main/index.html', **params)


class LoginHandler(BaseHandler):

    @classmethod
    def get_or_create_user(cls):
        try:
            user = models.User.select().get()
        except models.DoesNotExist:
            user = models.User(name='Test', email='Test@email.com')
            user.save()
        return user

    @gen.coroutine
    def get(self):

        user = yield self.run_async(self.get_or_create_user)
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
