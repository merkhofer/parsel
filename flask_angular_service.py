#!/usr/bin/env python

import os, errno
import sys
import json
import shutil
import pprint

#PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
#sys.path.append(PROJECT_ROOT)
#sys.path.append(os.path.join(PROJECT_ROOT, ".."))

from flask_jsonpify import jsonify
from cross_domain import crossdomain

from flask import Flask,request,abort,Response,make_response
from werkzeug.routing import BaseConverter

app = Flask(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler(401)
def custom_401(error):
    return Response('Not authorized to access file(s)', 401, {'WWWAuthenticate':'Basic realm="Session id Required"'})

@app.errorhandler(404)
def custom_404(error):
    return Response('Requested listing cannot be found', 404, {})
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Catch-all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@crossdomain(origin='*')
def catch_all(path):
    return '''
        ''' % globals()

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8000)
