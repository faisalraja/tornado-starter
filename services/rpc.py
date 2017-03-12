import logging
import time
from tornado import gen
import config
from config import mc
from tornado.concurrent import run_on_executor
import urllib.request
from lib import utils
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException, Client
import models


class ApiHandler(RpcHandler):

    async def wait(self):
        # Await on any thread
        r = await self.run_async(self._wait, 3)
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

    def _wait(self, n):
        time.sleep(n)
        return 'Waited {}'.format(n)

    async def post_db(self, create):

        def post(create=False):
            if create:
                post = models.Post(title='hello', content='world')
                post.save()
            else:
                post = models.Post.select().get()
            return post

        p = await self.run_async(post, create)
        return p.title

    @classmethod
    def test_worker(cls, url):
        with urllib.request.urlopen(url) as resp:
            return resp.status

    async def cache_test(self, create):

        if create:
            val = await self.run_async(mc.set, 'test', '555', 5)
        else:
            val = await self.run_async(mc.get, 'test')
        return val

    async def worker_add(self, wait_for_result=False):
        result = await self.defer(ApiHandler.test_worker,
                                  'http://localhost:8080/?test=1'
                                  if config.is_local else 'https://tornadostarter.herokuapp.com/?test=1')

        if wait_for_result:
            result = await result
            return result
