import logging
from tornado import gen

import config
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException, Client


class ApiHandler(RpcHandler):

    def user_id(self):

        return 123

    async def login(self):
        # Async Samples
        await gen.sleep(3)
        return True

    async def logout(self):
        client = Client('http://localhost:8080/rpc' if config.is_local else 'https://tornadostarter.herokuapp.com/rpc')
        return await client.login()

    def is_logged_in(self):

        return False

    def hello(self, world, limit=1):

        return [world for i in range(limit)]

    def sample_error(self):
        # this is good for any types of errors
        raise ServerException('Just a sample error')