import logging
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):

        params = {}
        return self.render_template('admin/index.html', **params)