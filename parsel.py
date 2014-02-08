#!/usr/bin/python

from flask import Flask,request,render_template
import sys
import os
import nltk_magic

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, ".."))
app = Flask(__name__,template_folder=PROJECT_ROOT + '/htmls')

@app.template_filter('is_list')
def is_list(some_object):
    return isinstance(some_object, list)

@app.route('/')
def get_params():
    return render_template("parsel-get.html")

@app.route('/', methods=['POST'])
def my_form_post():
    processes = {}
    text = request.form['text']
    if not text:
        return "Where's the text? I'm not making a pretty page for this... press back."
    for process in ['sent_tokenize', 'pos_tag', 'make_bag', 'chunk', 'extract_relations']:
        processes[process] = request.form.get(process)
    t_type = request.form.get('tokenizer')
    #TODO: shouldn't mess with regex if not relevant
    t_regex = request.form.get('token_regex')    
    processes['tokenizer_type'] = (t_type, t_regex)
    results = nltk_magic.nltk_magic(text, processes)
    return render_template("parsel-results.html", results=results)
 


if __name__ == '__main__':
#    app.debug = True
    app.run()
