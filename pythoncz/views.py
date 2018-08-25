import os
import subprocess
from fnmatch import fnmatch
from urllib.parse import quote_plus as url_quote_plus

from arrow import Arrow
from flask import (render_template as _render_template, url_for,
                   request, make_response, send_from_directory, Response)

from pythoncz import app, freezer
from pythoncz.models import jobs, photos, beginners, github, events


# Templating

def render_template(filename, **kwargs):
    kwargs['template_url'] = app.config['TEMPLATES_DIR_URL'] + filename
    return _render_template(filename, **kwargs)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter('urlencode')
def urlencode_filter(s):
    return url_quote_plus(str(s).encode('utf8'))


@app.template_filter('format_arrow')
def format_arrow_filter(dt: Arrow):
    return dt.to("Europe/Prague").strftime("%H:%M %d. %m. %Y")


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


@app.route('/udalosti/')
def events_cs():
    return render_template('events_cs.html', data=events.data)


@app.route('/en/events/')
def events_en():
    return render_template('events_en.html', lang='en', data=events.data)


@app.route("/events.ics")
def events_ical():
    return Response(str(events.get_calendar()), mimetype="text/calendar")


@app.route('/zapojse/')
def get_involved_cs():
    disabled = os.getenv('DISABLE_GITHUB_ISSUES_FETCH', False)
    try:
        if disabled:
            raise Exception('DISABLE_GITHUB_ISSUES_FETCH is set')
        issues = github.get_issues(app.config['GITHUB_ORGANIZATIONS'])
        return render_template('get_involved_cs.html', issues=issues)
    except Exception as e:
        template = render_template('get_involved_cs.html', issues=[], error=e)
        code = 200 if disabled else 500
        return make_response(template, code)


# Redirects of legacy stuff

def redirect(url, code=None):
    """Return a response with a Meta redirect, code is unused"""

    # With static pages, we can't use HTTP redirects.
    # Return a page wit <meta refresh> instead.
    #
    # When Frozen-Flask gets support for redirects
    # (https://github.com/Frozen-Flask/Frozen-Flask/issues/81),
    # this should be revisited.

    return render_template('meta_redirect.html', url=url)


@app.route('/english.html')
def index_en_legacy():
    return redirect(url_for('index_en'), code=301)


@app.route('/pyladies/<path:target>')
def pyladies(target):
    return redirect('http://pyladies.cz/v1/' + target, code=301)


@freezer.register_generator
def pyladies():
    # This is hardcoded because it doesn't change & it's easier to hardcode it
    targets = (
        's001-install/',
        's002-hello-world/',
        's003-looping/',
        's004-strings/',
        's005-modules/',
        's006-lists/',
        's007-cards/',
        's008-cards2/',
        's009-git/',
        's010-data/',
        's011-dicts/',
        's012-pyglet/',
        's014-class/',
        's015-asteroids/',
        's016-micropython/',
    )
    yield from ({'target': t} for t in targets)


@app.route('/pyladies/')
def pyladies_index():
    return redirect('http://pyladies.cz/', code=301)


# Talks, this used to redirect, but that's not possible with *.pdf HTML files
talks_dir = 'talks-archive'


@app.before_first_request
def clone_talks():
    try:
        os.chdir(talks_dir)
    except FileNotFoundError:
        subprocess.run(('git', 'clone',
                         'https://github.com/pyvec/talks-archive',
                         '--depth', '1'))
        os.chdir(talks_dir)
    else:
        subprocess.run(('git', 'fetch', 'origin'), check=True)
        subprocess.run(('git', 'reset', '--hard', 'origin/master'), check=True)
    finally:
        os.chdir('..')


@app.route('/talks/<path:target>')
def talks(target):
    # sends from pythoncz directory, hence ../
    return send_from_directory(f'../{talks_dir}', target)


@freezer.register_generator
def talks():
    ignore = ['.travis.yml', '.gitignore']
    for name, dirs, files in os.walk(talks_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file == '.git':
                continue
            if not any(fnmatch(file, ig) for ig in ignore):
                path = os.path.relpath(os.path.join(name, file), talks_dir)
                yield {'target': path}
