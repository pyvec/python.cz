from flask import (render_template as _render_template, url_for,
                   redirect, request)

from pythoncz import app
from pythoncz.models import jobs, photos, beginners, github


# Templating

def render_template(filename, **kwargs):
    kwargs['template_url'] = app.config['TEMPLATES_DIR_URL'] + filename
    return _render_template(filename, **kwargs)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def inject_context():
    return {
        'debug': app.debug,
        'config': app.config,
        'url': request.url,
        'lang': 'cs',
    }


# Regular views

@app.route('/')
def index_cs():
    return render_template('index_cs.html',
                           photo_urls=photos.get_random_urls(5))


@app.route('/en/')
def index_en():
    return render_template('index_en.html',
                           photo_urls=photos.get_random_urls(5), lang='en')


@app.route('/zacatecnici/')
def beginners_cs():
    return render_template('beginners_cs.html', data=beginners.data)


@app.route('/prace/')
def jobs_cs():
    return render_template('jobs_cs.html', data=jobs.data)


@app.route('/en/jobs/')
def jobs_en():
    return render_template('jobs_en.html', data=jobs.data, lang='en')


@app.route('/zapojse/')
def get_involved_cs():
    issues = github.get_issues(app.config['GITHUB_ORGANIZATIONS'])
    return render_template('get_involved_cs.html', issues=issues)


# Subdomain redirect

@app.route('/', subdomain='www')
def subdomain_redirect():
    return redirect(url_for('index_cs'))


# Redirects of legacy stuff

@app.route('/index.html')
def index_legacy():
    return redirect(url_for('index_cs'), code=301)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)


@app.route('/pyladies/<path:target>')
def pyladies(target):
    return redirect('http://pyladies.cz/v1/' + target, code=301)


@app.route('/pyladies/')
def pyladies_index():
    return redirect('http://pyladies.cz', code=301)


@app.route('/talks/<path:target>')
def talks(target):
    base_url = 'https://github.com/pyvec/talks-archive/raw/master/'
    return redirect(base_url + target, code=301)
