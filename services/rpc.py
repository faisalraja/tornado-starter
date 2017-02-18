import logging
from tornado import gen
import config
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException, Client


class ApiHandler(RpcHandler):

    async def wait(self):
        # Async Samples
        await gen.sleep(3)
        return True

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
