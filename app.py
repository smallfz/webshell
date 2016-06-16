#-*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.append(_dir)

from flask import Flask, redirect, request
from flask import render_template, make_response
from flask import abort
import re
import subprocess
import tempfile


app = Flask(__name__, template_folder='templates')
app.debug = True



def _invoke_shell(filepath):
    _path = os.path.abspath(filepath)
    _tdir = tempfile.gettempdir()
    out = None
    try:
        tname = '%s.tmp' % os.urandom(8).encode('hex')
        tpath = os.path.join(_tdir, tname)
        out = open(tpath, 'wb+')
        rc = subprocess.call([_path], 
                             shell=True,
                             stdout=out,
                             stderr=out)
        out.write('\r\n')
        out.write('[return %s]' % rc)
        out.seek(0)
        return out.read()
    finally:
        if out:
            out.close()

@app.route('/git-hook/<script_name>')
def run_script(script_name):
    script_dir = os.path.abspath(os.path.join(_dir, 'shell'))
    # if not os.path.isdir(script_dir):
    #     os.makedir(script_dir)
    pt = r'^[\w\.]+$'
    if not re.search(pt, script_name, re.I|re.S):
        return abort(400)
    script_path = os.path.join(script_dir, script_name)
    if not os.path.isfile(script_path):
        return abort(404)
    elif not os.access(script_path, os.X_OK):
        return abort(403)
    output = _invoke_shell(script_path)
    resp = make_response(output)
    resp.content_type = 'text/plain'
    return resp


if __name__ == '__main__':
    port = 9990
    _argv = sys.argv[1:]
    if _argv and _argv[0].isdigit():
        port = int(_argv[0])
    host = ('127.0.0.1', port)
    print 'serving port: %s' % port
    app.run(host=host[0], port=host[1], debug=True)


