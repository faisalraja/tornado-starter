import json
import logging
import datetime
from functools import wraps
from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.platform.asyncio import to_tornado_future
import config
from lib import jsonrpc, utils
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from models import models


def tasklet(method):
    """Runs a function on a new thread and uses RequestHandler.executor"""
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        fut = self.executor.submit(method, self, *args, **kwargs)
        return await to_tornado_future(fut)
    return wrapper


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
    """
    executor = ThreadPoolExecutor(max_workers=config.max_workers)

    async def prepare(self):
        user_id = self.get_secure_cookie('user_id')

        if user_id:
            self.current_user = await self.run_async(models.User.get_by_id, user_id)

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

    @tasklet
    def run_async(self, fn, *args, **kwargs):

        return fn(*args, **kwargs)

    @classmethod
    async def deferred_result(cls, job):
        while True:
            await gen.sleep(0.5)
            if job.result is not None or job.status == 'failed':
                break
        return job.result

    @tasklet
    def defer(self, fn, *args, **kwargs):
        q = utils.get_queue()
        job = q.enqueue(fn, *args, **kwargs)
        return BaseHandler.deferred_result(job)

    def data_received(self, chunk):
        pass


class RpcHandler(BaseHandler):

    async def post(self):
        server = jsonrpc.Server(self)
        result = await server.handle(self.request)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))
        self.finish()


