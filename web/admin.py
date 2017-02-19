import logging
from tornado import web
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    @web.authenticated
    def get(self):

        params = {}
        return self.render_template('admin/index.html', **params)