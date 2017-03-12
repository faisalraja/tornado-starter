import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import logging
import tornado
import config
import routes
from lib import utils, basemodel
import models


def setup_db():
    config.db.connect()
    config.db.create_tables(list(utils.get_members_by_parent(models, basemodel.BaseModel).values()), safe=True)
    config.db.close()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = routes.get_routes()

        settings = dict(
            site_title=config.project_name,
            cookie_secret=config.cookie_secret,
            template_path=utils.get_path('templates'),
            static_path=utils.get_path('static'),
            xsrf_cookies=False,  # before enabling read: http://www.tornadoweb.org/en/stable/guide/security.html
            debug=config.is_local,
            autoreload=config.is_local,
            login_url='/login'
        )

        tornado.web.Application.__init__(self, handlers, **settings)


logging.getLogger().setLevel(logging.DEBUG)
setup_db()

application = Application()

if __name__ == '__main__':
    define('port', default='8080', help='Listening port', type=str)
    tornado.options.parse_command_line()
    port = os.getenv('PORT', options.port)
    print("Server listening on port " + str(port))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
