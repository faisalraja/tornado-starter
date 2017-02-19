import json
import logging
import datetime
from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import config
from lib import jsonrpc, utils
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


class BaseHandler(web.RequestHandler, JinjaRenderer):
    """
        BaseHandler for all requests
\    """
    executor = ThreadPoolExecutor(max_workers=config.max_workers)

    @gen.coroutine
    def prepare(self):
        user_id = self.get_secure_cookie('user_id')

        if user_id:
            self.current_user = yield self.run_async(models.User.get_by_id, user_id)

    @property
    def path_url(self):

        return '{}://{}{}'.format(self.request.protocol, self.request.host, self.request.path)

    def is_ajax(self):

        return self.request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'

    def render_template(self, template_name, **kwargs):

        kwargs.update({
            'static_url': self.settings.get('static_url_prefix', '/static/'),
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
            'now': datetime.datetime.now(),
            'user': self.current_user
        })
        self.write(self.render_jinja(template_name, **kwargs))
        self.finish()

    @run_on_executor
    def run_async(self, fn, *args, **kwargs):

        return fn(*args, **kwargs)

    @classmethod
    @gen.coroutine
    def background_result(cls, job):
        while True:
            yield gen.sleep(0.1)
            if job.result is not None or job.status == 'failed':
                break
        return job.result

    @run_on_executor
    def run_background(self, fn, *args, **kwargs):
        q = utils.get_queue()
        job = q.enqueue(fn, *args, **kwargs)
        return BaseHandler.background_result(job)


class RpcHandler(BaseHandler):

    async def post(self):
        server = jsonrpc.Server(self)
        result = await server.handle(self.request)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))
        self.finish()


