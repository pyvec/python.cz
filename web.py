# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, redirect


app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index'), code=301)


@app.route('/english.html')
def index_en():
    return render_template('english.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
