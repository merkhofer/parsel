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

import config
import tarfile


app = Flask(__name__)

WALK_DIR='/two/Music'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler(401)
def custom_401(error):
    return Response('Not authorized to access file(s)', 401, {'WWWAuthenticate':'Basic realm="Session id Required"'})

@app.errorhandler(404)
def custom_404(error):
    return Response('Requested listing cannot be found', 404, {})
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Pass directory or file listing data out.
@app.route("/source/<string:source>/listing/<int:listing_type>/list/", methods=['GET'])

@crossdomain(origin='*')

def retrieve_listing(file_container_id,source='CTS'):

    if 'dir' in source:

        if listing_type == 1:
            # 1 = short listing
            root, dirs, files = os.walk(WALK_DIR)
            resp = jsonify({
                'root':root,
                'dirs':dirs,
                'files':files
                })
           return resp

        elif listing_type == 2:

            # 2 = long listing
            for root, dirs, files in os.walk(WALK_DIR):
                path = root.split('/')
                print (len(path) - 1) *'---' , os.path.basename(root)       

                for file in files:
                    print len(path)*'---', file
        else:
            abort(404)

    elif 'tar' in source:
        t = tarfile.open('example.tar', 'r')
        return jsonify({'names': t.getnames() })

    else: 
        raise Exception("Unknown option: %s" % source)

    #print "Response:",resp.headers,resp.response


@app.route("/source/<string:source>/contents/<regex('.*'):filename>/", 
    methods=['GET','POST','DELETE'])
def individual_files(source,filename):
    session_id = checkfor_session_cookie()

    if request.method == 'GET':
       # stream file here... 
       pass

    elif request.method == 'DELETE':
        # Living dangerously...
        try:
            os.remove(filename)
            return  jsonify({
                'results':'purged %s' % full_file
                })

        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

            '''
            Trying to delete a file that is not present is not 
            considered an error here.
            '''
            return jsonify({
               'results':'file not present: %s' % full_file
                })


if __name__ == '__main__':
    app.run(debug=True, host=127.0.0.1, port=5000)
