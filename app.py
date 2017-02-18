"""
This is designed more for backend developers building quick prototypes
If you want to optimize your frontend you should probably start with
using less and having a script the merge and compress them
"""
import asyncio
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
import logging
import tornado
import config
import routes
from lib import utils
from models import models

define('port', default='8080', help='Listening port', type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = routes.get_routes()

        settings = dict(
            site_title=config.project_name,
            cookie_secret=config.cookie_secret,
            template_path=utils.get_path('templates'),
            static_path=utils.get_path('static'),
            xsrf_cookies=False,  # before enabling read: http://www.tornadoweb.org/en/stable/guide/security.html
            debug=config.is_local
        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    AsyncIOMainLoop().install()
    tornado.options.parse_command_line()

    print("Server listening on port " + str(options.port))
    logging.getLogger().setLevel(logging.DEBUG)

    app = Application()
    app.listen(port=options.port)
    # app.objects = peewee_async.Manager(database)
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Server stopped')
