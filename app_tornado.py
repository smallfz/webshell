#-*- coding: utf-8 -*-

import os, sys, signal

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

import logging
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import argparse as ap

try:
    import daemonize
except ImportError:
    daemonize = None

logger = logging.getLogger(__name__)
lh = logging.FileHandler(os.path.join(_dir, 'app.log'), 'w')
lh.setLevel(logging.DEBUG)
logger.addHandler(lh)

from app import app

config = {
    'port': 9990
}

def server():
    port = config['port']
    print 'serving port: %s' % port
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
        keep_fds = [lh.stream.fileno()]
        daemon = daemonize.Daemonize(app='webshell',
                                     pid=pid,
                                     logger=logger,
                                     keep_fds=keep_fds,
                                     action=server)
        if args.cmd == 'start':
            daemon.start()
        elif args.cmd == 'stop':
            if os.path.isfile(pid) and os.access(pid, os.R_OK):
                with open(pid, 'rb') as f:
                    _pid = int(f.read().strip())
                    if _pid:
                        os.kill(_pid, signal.SIGTERM)
    else:
        server()

