#!/usr/bin/env python

import os, errno
import sys
import re
import json
import shutil
import pprint

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, ".."))

from inc.flask_jsonpify import jsonify
from inc.cross_domain import crossdomain

from flask import Flask,request,abort,Response,make_response
from werkzeug.routing import BaseConverter

import tarfile


app = Flask(__name__)

# Change this directory to some dir on your machine. Only run this locally, don't run online.
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
class DirWalker(object):
    def __init__(self,directory,level=None,match_regex=None,debug=True):
        self.level = level # None = traverse whole tree
        self.directory = directory
        self.debug = debug
        self.match_regex = match_regex
        self.all_roots = []
        self.all_dirs = []
        self.all_files = []

    def walkit(self):
        self.all_roots = []
        self.all_dirs = []
        self.all_files = []
        level_traverse = 0
        for root, dirs, files in os.walk(self.directory):
            if self.level and (level_traverse >= self.level):
                break

            level_traverse += 1
            path = root.split('/')
            if self.debug:
                print (len(path) - 1) *'---' , os.path.basename(root)       

                for file in files:
                    print len(path)*'---', file

            if self.match_regex:
                # "re.match" matches the beginning of the string.
                # This match is not context aware. Feel free to change it!
                if re.match(self.match_regex,root):
                    self.all_roots.append(root) 
                self.all_dirs += [x for x in dirs if re.match(self.match_regex,x)]
                self.all_files += [x for x in files if re.match(self.match_regex,x)]
            else:
                self.all_roots += [root]
                self.all_dirs += dirs
                self.all_files += files

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Pass directory or file listing data out.
@app.route("/source/<string:source>/listing/<int:listing_type>/startswith/<string:startswith>/", 
    methods=['GET',])
@app.route("/source/<string:source>/listing/<int:listing_type>/", 
    defaults={'startswith':None},methods=['GET',])
@crossdomain(origin='*')

def retrieve_listing(source,listing_type,startswith):

    # Generate regex that will match on any combo of lower and upper case.
    starts_lu = None
    if startswith:
        starts_lu = ''.join(['[' + x.lower() + x.upper() + ']' for x in startswith])

    if 'dir' in source:

        dw = DirWalker(directory=WALK_DIR, match_regex=starts_lu)

        if listing_type == 1:
            # 1 = short listing
            dw.level=1
            dw.walkit()
            return jsonify({
                'matched_pattern':starts_lu,
                'root':dw.all_roots[0] if dw.all_roots else None,
                'dirs':dw.all_dirs,
                'files':dw.all_files
                })

        elif listing_type == 2:
            # 2 = long listing
            dw.walkit()
            return jsonify({
                'matched_pattern':starts_lu,
                'roots':dw.all_roots,
                'dirs':dw.all_dirs,
                'files':dw.all_files
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


@app.route("/contents/<regex('.*'):file_startswith_regex>/dir/<path:dirname>", 
    methods=['GET','POST','DELETE'])
@crossdomain(origin='*')
def individual_files(dirname,file_startswith_regex):

    dirname = '/' + dirname
    if request.method == 'GET':
        # Instead of constructing regex, yours is passed stright through to the search.
        # Don't run this on a publicly accessible server, this is a giant security hole. 
        dw = DirWalker(directory=dirname,match_regex=file_startswith_regex)
        dw.walkit()
        return jsonify({
            'matched_pattern':file_startswith_regex,
            'walked directory':dirname,
            'root':dw.all_roots[0] if dw.all_roots else None,
            'dirs':dw.all_dirs,
            'files':dw.all_files
            })

    elif request.method == 'POST':
        return jsonify({
           'results':'Do some update here, maybe?'
            })

    elif request.method == 'DELETE':
        pass
        '''
        # Living dangerously...
        try:
            os.remove('some match here...')
            return  jsonify({
                'results':'purged %s' % file_startswith_regex
                })

        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

            
            Trying to delete a file that is not present is not 
            considered an error here.
           
            return jsonify({
               'results':'file not present: %s' % file_startswith_regex
                })
        '''

# Catch-all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@crossdomain(origin='*')
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
http://%(HOST)s:%(PORT)s/contents/some_regex/dir/dirname<br>
        ''' % globals()

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
