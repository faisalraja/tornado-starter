import logging
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException

ERROR_LOGIN = 'Login Error'
TYPE_ERROR = 'error'


# Sample json rpc
class ApiHandler(RpcHandler):

    def user_id(self):

        return 123

    def login(self):

        return True

    def logout(self):

        return False

    def is_logged_in(self):

        return False

    def hello(self, world, limit=1):

        return [world for i in range(limit)]

    def sample_error(self):
        # this is good for any types of errors
        raise ServerException('Just a sample error')