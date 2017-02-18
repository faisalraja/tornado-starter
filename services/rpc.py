import logging
import time
from tornado import gen
import config
from config import memcache
from tornado.concurrent import run_on_executor
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException, Client
from models import models


class ApiHandler(RpcHandler):

    @gen.coroutine
    def wait(self):
        # Await on any thread
        r = yield self._wait(3)
        return r

    async def client_call_wait(self):
        client = Client('http://localhost:8080/rpc' if config.is_local else 'https://tornadostarter.herokuapp.com/rpc')
        return await client.wait()

    def hello(self, world, limit=1):

        return [world for i in range(limit)]

    def sample_error(self):
        # this is good for any types of errors
        raise ServerException('Just a sample error')

    def add(self, a, b):

        return a + b

    @run_on_executor
    def _wait(self, n):
        time.sleep(n)
        return 'Waited {}'.format(n)

    @run_on_executor
    def _db(self, create=False):
        if create:
            post = models.Post(title='hello', content='world')
            post.save()
        else:
            post = models.Post.select().get()
        return post

    @run_on_executor
    def _set_cache(self, key, value, timeout=5):
        return memcache.set(key, value, timeout)

    @run_on_executor
    def _get_cache(self, key):
        return memcache.get(key)

    @gen.coroutine
    def post_db(self, create):
        p = yield self._db(create)
        return p.title

    @gen.coroutine
    def cache_test(self, create):
        if create:
            val = yield self._set_cache('test', '555')
        else:
            val = yield self._get_cache('test')
        return val