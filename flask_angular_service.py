#!/usr/bin/env python

import os, errno
import sys
import json
import shutil
import pprint

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, ".."))

from inc.flask_jsonpify import jsonify
from inc.cross_domain import crossdomain

from flask import Flask,render_template, send_from_directory
from werkzeug.routing import BaseConverter

# Note the custom template directory.
app = Flask(__name__,template_folder='./htmls')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler(401)
def custom_401(error):
    return Response('Not authorized to access file(s)', 401, {'WWWAuthenticate':'Basic realm="Session id Required"'})

@app.errorhandler(404)
def custom_404(error):
    return Response('Requested listing cannot be found', 404, {})
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Flask automatically serves templates and static from their respetive directory names.
# I customize them below.
# This is for demo purposes. A Better way to serve your static content is via nginx.

@app.route('/js/<path:filename>')
def custom_js_static(filename):
    return send_from_directory('./js/', filename)

@app.route('/css/<path:filename>')
def custom_css_static(filename):
    return send_from_directory('./css/', filename)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Catch-all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@crossdomain(origin='*')
def catch_all(path):
    return render_template('angular_file_tar.html', var="value")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8000)
