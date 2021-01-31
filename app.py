import json
import os
from flask import Flask, request, render_template
from flask.blueprints import Blueprint
from keywords_extractor import keywords
from saving import save_new
import wikipedia_search
import top_keys

blp = Blueprint("Main", __name__)


@blp.route('/')
@blp.route('/add/', methods=['post', 'get'])
def add():
    message = ''
    input_text = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text')
    if input_text != '':
        message = input_text
    else:
        message = ""
    return render_template('add.html', message=message, save_flag=False, wiki_flag=False)


@blp.route('/add/find', methods=['post', 'get'])
def add_find():
    message = ''
    input_text = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text')
    if input_text != '':
        table = keywords(input_text)
        # message = ", ".join(keywords_list)
    else:
        message = ""
    return render_template('add.html',
                           message=message,
                           save_flag=True,
                           wiki_flag=True,
                           text=input_text,
                           table=table,
                           table_json=json.dumps(table))


@blp.route('/add/save', methods=['post', 'get'])
def add_save():
    keywords_raw = ''
    input_text = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        keywords_raw = request.form.get('keywords')
    if input_text != '':
        save_new(input_text, keywords_raw)
    return render_template('add.html')


@blp.route('/add/wiki', methods=['post', 'get'])
def add_wiki():
    input_text = ''
    keywords_raw = ''
    table = []
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        keywords_raw = request.form.get('keywords')
        keywords_list = json.loads(keywords_raw)
        table = wikipedia_search.list_summary(keywords_list)

    return render_template('add.html',
                           save_flag=True,
                           wiki_flag=True,
                           text=input_text,
                           table=table,
                           table_json=json.dumps(table))


@blp.route('/top_key/', methods=['get'])
def all_texts():
    table = top_keys.top_keys()
    return render_template('top.html', table=table)



def create_app(db_name: str = 'test'):
    secret = os.urandom(32)
    _app = Flask(__name__)
    _app.config['SECRET_KEY'] = secret
    _app.register_blueprint(blp)
    return _app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=80, host='127.0.0.1')
