from flask import Flask
from flask import request
from flask import render_template,flash
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
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    processes = {}
    text = request.form['text']
    processes['sent_tokenize'] = request.form.get('sent_tokenizer')
    #tuple of tokenizer type and regex. If irrelevant, regex is ignored
    t_type = request.form.get('tokenizer')
    processes['tokenizer_type'] = (t_type, '')
    processes['pos_tag'] = request.form.get('pos_tag')
    processes['make_bag'] = request.form.get('make_bag')
    results = nltk_magic.nltk_magic(text, processes)
    return str(processes)
    #return render_template("results.html", results=results)

@app.route('/tasks/', methods=['GET','POST'])
def new_task():
    if request.method == 'POST':
        tts = request.form['name']
        #flash(str(tts)+'is being selected')
        ms = request.form['mymultiselect[]']
        return "{} {}".format(ms, tts)
    return render_template("new-task.html")    


if __name__ == '__main__':
    app.debug = True
    app.run()