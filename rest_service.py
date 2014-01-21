#!/usr/bin/env python

import os, errno
import sys
import re
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

import tarfile


app = Flask(__name__)

WALK_DIR='/two/Music'
TAR_FILE='example.tar'
HOST="127.0.0.1"
PORT=7000

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
@app.route("/source/<string:source>/listing/<int:listing_type>/startswith/<string:startswith>/", 
    methods=['GET',])
@app.route("/source/<string:source>/listing/<int:listing_type>/", 
    defaults={'startswith':None},methods=['GET',])
@crossdomain(origin='*')

def retrieve_listing(source,listing_type,startswith):

    starts_lu = None
    if startswith:
        starts_lu = ''.join(['[' + x.lower() + x.upper() + ']' for x in startswith])

    if 'dir' in source:

        if listing_type == 1:
            # 1 = short listing
            root, dirs, files = os.walk(WALK_DIR).next()
            if starts_lu:
                dirs = [x for x in dirs if re.match(starts_lu,x)]
                files = [x for x in files if re.match(starts_lu,x)]
            return jsonify({
                'matched_pattern':starts_lu,
                'root':root,
                'dirs':dirs,
                'files':files
                })

        elif listing_type == 2:

            # 2 = long listing
            all_roots = []
            all_dirs = []
            all_files = []
            for root, dirs, files in os.walk(WALK_DIR):
                path = root.split('/')
                print (len(path) - 1) *'---' , os.path.basename(root)       

                for file in files:
                    print len(path)*'---', file

                if starts_lu:
                    if re.match(starts_lu,root):
                        all_roots.append(root) 
                    all_dirs += [x for x in dirs if re.match(starts_lu,x)]
                    all_files += [x for x in files if re.match(starts_lu,x)]
                else:
                    all_roots += root
                    all_dirs += dirs
                    all_files += files

            return jsonify({
                'matched_pattern':starts_lu,
                'roots':all_roots,
                'dirs':all_dirs,
                'files':all_files
                })
        else:
            abort(404)

    elif 'tar' in source:
        t = tarfile.open(TAR_FILE, 'r')

        # Only one listing type for tar files.
        listing = t.getnames()

        if starts_lu:
            listing = [x for x in listing if re.match(starts_lu,x)]

        return jsonify({'names': listing, 'tarfile': TAR_FILE})

    else: 
        raise Exception("Unknown option: %s" % source)

    #print "Response:",resp.headers,resp.response


@app.route("/dir/<string:dirname>/contents/<regex('.*'):filename>/", 
    methods=['GET','POST','DELETE'])
@crossdomain(origin='*')
def individual_files(source,fileregex):

    if request.method == 'GET':
        if 'dir' in source:
            pass
        elif 'tar' in source:
            pass

    elif request.method == 'POST':
        return jsonify({
           'results':'Do some update here, maybe?'
            })

    elif request.method == 'DELETE':
        # Living dangerously...
        try:
            os.remove(filename)
            return  jsonify({
                'results':'purged %s' % filename
                })

        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

            '''
            Trying to delete a file that is not present is not 
            considered an error here.
            '''
            return jsonify({
               'results':'file not present: %s' % filename
                })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return '''
<br>
Your options: <br>
<br>
http://%(HOST)s:%(PORT)s/source/dir/listing/1<br>
http://%(HOST)s:%(PORT)s/source/dir/listing/2<br>
http://%(HOST)s:%(PORT)s/source/dir/listing/1/startswith/N<br>
http://%(HOST)s:%(PORT)s/source/dir/listing/2/startswith/N<br>
http://%(HOST)s:%(PORT)s/source/tar/listing/1/startswith/N<br>
        ''' % globals()

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
