import os

import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

from user.views import RegisterHandler, InitDBHandler, LoginHandler

define('port', default=8000, type=int)


def make_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return tornado.web.Application(handlers=[
        ('/register/', RegisterHandler),
        ('/init_db/', InitDBHandler),
        ('/login/', LoginHandler),
    ],
        template_path=os.path.join(BASE_DIR, 'templates'),
        static_path=os.path.join(BASE_DIR, 'static')
    )


if __name__ == '__main__':
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
