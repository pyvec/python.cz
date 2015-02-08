# -*- coding: utf-8 -*-


from flask import (Flask, render_template as _render_template, url_for,
                   redirect, request)


# This settings ensure that Flask templates are in the root of the application
app = Flask(__name__,
            static_folder='.',
            static_url_path='',
            template_folder='.')


def render_template(filename, **kwargs):
    kwargs['github_url'] = (
        'https://github.com/pyvec/python.cz/blob/master/' + filename
    )
    return _render_template(filename, **kwargs)


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'url': 'http://python.cz' + request.path
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/index-en.html')
def index_en():
    return render_template('index-en.html')


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
