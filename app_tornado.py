#-*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import argparse as ap

try:
    import daemonize
except ImportError:
    daemonize = None


from app import app

config = {
    'port': 9990
}

def server():
    port = config['port']
    print 'serving port: %s' % port
    return
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port, address='127.0.0.1')
    IOLoop.instance().start()
    

if __name__ == '__main__':
    parser = ap.ArgumentParser(description=u'Run a webshell server.')
    parser.add_argument('cmd', choices=['start', 'stop'])
    parser.add_argument('--port',
                        default=config['port'],
                        type=int,
                        required=False,
                        help='http port, default 9990')

    args = parser.parse_args()
    config['port'] = args.port
    if daemonize and sys.platform != 'win32':
        pid = '/var/run/webshell.pid'
        daemon = Daemonize(app='webshell', pid=pid, action=server)
        if args.cmd == 'start':
            daemon.start()
        elif args.cmd == 'stop':
            daemon.exit()
    else:
        server()

