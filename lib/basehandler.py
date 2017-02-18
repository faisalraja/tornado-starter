import json
import logging
import datetime
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import config
from lib import jsonrpc
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from models import models


class JinjaRenderer:
    """
    A simple class to hold methods for rendering templates.
    """
    def render_jinja(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings['template_path']
            )

        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, JinjaRenderer):
    """
        BaseHandler for all requests
\    """
    executor = ThreadPoolExecutor(max_workers=config.max_workers)

    # def prepare(self):
    #     print('Connect')
    #     models.db.connect()
    #
    # def on_finish(self):
    #     print('Close')
    #     if not models.db.is_closed():
    #         models.db.close()

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def is_ajax(self):

        return self.request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'

    def render_template(self, template_name, **kwargs):

        kwargs.update({
            'static_url': self.settings.get('static_url_prefix', '/static/'),
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
            'year': datetime.datetime.now().year
        })
        self.write(self.render_jinja(template_name, **kwargs))
        self.finish()


class RpcHandler(BaseHandler):

    async def post(self):
        server = jsonrpc.Server(self)
        result = await server.handle(self.request)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))
        self.finish()


