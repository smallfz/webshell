#-*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop


from app import app



if __name__ == '__main__':
    port = 9990
    _argv = sys.argv[1:]
    if _argv and _argv[0].isdigit():
        port = int(_argv[0])

    print 'serving port: %s' % port

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port, address='127.0.0.1')
    IOLoop.instance().start()

