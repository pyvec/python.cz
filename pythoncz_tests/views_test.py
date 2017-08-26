from urllib.parse import quote_plus as url_quote_plus

import pytest
from flask import url_for
from werkzeug.contrib.cache import NullCache

from pythoncz import app
from pythoncz.models import github as github_module


def create_issue(**kwargs):
    issue = {
        'title': 'Test Issue',
        'html_url': 'http://github.com/pyvec/zapojse/issues/42',
        'updated_at': '2017-02-07T16:52:01Z',
        'user': {
            'login': 'encukou',
            'html_url': 'https://github.com/encukou',
        },
        'is_pull_request': False,
        'repository_name': 'zapojse',
        'repository_url_html': 'http://github.com/pyvec/zapojse/',
        'organization_name': 'pyvec',
        'comments': 5,
        'participants': 6,
        'votes': 3,
        'labels': ['bug'],
        'coach': False,
        'sprint-idea': False,
    }
    for key, value in kwargs.items():
        issue[key] = value
    return issue


@pytest.fixture
def test_client():
    app.testing = True
    with app.test_client() as client:
        yield client
    app.testing = False


@pytest.fixture()
def github():
    """Provides the 'github' module with everything mocked"""
    original_cache = github_module.cache
    original_get_issues = github_module.get_issues

    github_module.cache = NullCache()
    github_module.get_issues = lambda self, *args, **kwargs: []

    yield github_module

    github_module.cache = original_cache
    github_module.get_issues = original_get_issues


def test_get_involved_cs_no_issues(github, test_client):
    response = test_client.get('/zapojse/')

    assert response.status_code == 200


def test_get_involved_cs(github, test_client):
    def get_issues(self, *args, **kwargs):
        return [create_issue()]
    github.get_issues = get_issues
    response = test_client.get('/zapojse/')
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'Test Issue' in html
    assert 'http://github.com/pyvec/zapojse/issues/42' in html
    assert 'https://github.com/encukou' in html
    assert 'od encukou' in html
    assert 'komentářů: 5' in html
    assert 'účastníků diskuze: 6' in html
    assert 'hlasů: 3' in html
    assert 'fa-code-fork' not in html


@pytest.mark.parametrize('label_name,text,occurrences', [
    ('coach', 'Kouč pomůže!', 2),  # because it's mentioned also in the legend
    ('sprint-idea', 'Sprint', 1),
])
def test_get_involved_cs_labels(github, test_client,
                                label_name, text, occurrences):
    def get_issues(self, *args, **kwargs):
        return [create_issue(**{'labels': [label_name], label_name: True})]
    github.get_issues = get_issues
    response = test_client.get('/zapojse/')
    html = response.get_data(as_text=True)

    assert html.count(text) == occurrences


@pytest.mark.parametrize('repo_name,repo_linked,label', [
    ('pyvec/zapojse', False, None),
    ('pyvec/repo', True, None),
    ('pyladiescz/repo', True, 'label-pyladies'),
])
def test_get_involved_cs_repos(github, test_client,
                               repo_name, repo_linked, label):
    def get_issues(self, *args, **kwargs):
        return [create_issue(
            html_url='http://github.com/{}/issues/42'.format(repo_name),
            repository_name=repo_name.split('/')[1],
            repository_url_html='http://github.com/{}/'.format(repo_name),
            organization_name=repo_name.split('/')[0],
        )]
    github.get_issues = get_issues
    response = test_client.get('/zapojse/')
    html = response.get_data(as_text=True)

    if repo_linked:
        assert 'fa-code-fork' in html
        assert 'http://github.com/{}/'.format(repo_name) in html
    else:
        assert 'fa-code-fork' not in html
    if label:
        assert label in html


@pytest.mark.parametrize('is_pull_request,icon_name', [
    (True, 'fa-pencil-square'),
    (False, 'fa-exclamation-circle'),
])
def test_get_involved_cs_pull_request_icon(github, test_client,
                                           is_pull_request, icon_name):
    def get_issues(self, *args, **kwargs):
        return [create_issue(is_pull_request=is_pull_request)]
    github.get_issues = get_issues
    response = test_client.get('/zapojse/')
    html = response.get_data(as_text=True)

    assert icon_name in html


def test_get_involved_cs_error(github, test_client):
    def get_issues(self, *args, **kwargs):
        raise RuntimeError('Ouch!')
    github.get_issues = get_issues
    response = test_client.get('/zapojse/')
    html = response.get_data(as_text=True)

    assert response.status_code == 500
    assert 'issues-error' in html
    assert 'https://github.com/pyvec/zapojse/issues' in html
    assert '{base_url}?title={title}&amp;body={body}'.format(
        base_url='https://github.com/pyvec/python.cz/issues/new',
        title=url_quote_plus('Nefunguje Zapoj se'),
        body=url_quote_plus('RuntimeError: Ouch!'),
    ) in html


def test_index_legacy(test_client):
    response = test_client.get('/index.html')

    assert response.status_code == 301
    assert response.headers['location'] == url_for('index_cs', _external=True)


def test_index_en_legacy(test_client):
    response = test_client.get('/english.html')

    assert response.status_code == 301
    assert response.headers['location'] == url_for('index_en', _external=True)


def test_pyladies(test_client):
    response = test_client.get('/pyladies/foo/bar/baz.html')

    assert response.status_code == 301
    assert response.headers['location'] == (
        'http://pyladies.cz/v1/foo/bar/baz.html'
    )


def test_pyladies_index_trailing_slash(test_client):
    response = test_client.get('/pyladies/')

    assert response.status_code == 301
    assert response.headers['location'] == 'http://pyladies.cz'


def test_pyladies_index_without_trailing_slash(test_client):
    response = test_client.get('/pyladies')

    assert response.status_code == 301
    assert response.headers['location'] == (
        url_for('pyladies_index', _external=True)
    )


def test_talks(test_client):
    response = test_client.get('/talks/foo/bar/baz.html')

    assert response.status_code == 301
    assert response.headers['location'] == (
        'https://github.com/pyvec/talks-archive/raw/master/foo/bar/baz.html'
    )
