from urllib.parse import quote_plus as url_quote_plus

import pytest
from flask import url_for
from werkzeug.contrib.cache import NullCache

from pythoncz import app
from pythoncz.models import github as github_module


def generate_issue_mock(**kwargs):
    """
    Generates an issue fixture

    All attributes can be overriden by keyword arguments for the purpose
    of testing.
    """
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


def extract_issues_html(html):
    """
    Extracts the part of the HTML page, which contains the list of issues

    Testing the relevant part avoids getting false positives/negatives
    due to certain texts being present also in other parts of the page.
    """
    return html.split('id="issues"')[1]


@pytest.fixture
def test_client():
    """Flask app test client"""
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


def test_get_involved_cs_renders_ordinary_issue(github, test_client):
    def get_issues(self, *args, **kwargs):
        return [generate_issue_mock()]
    github.get_issues = get_issues

    response = test_client.get('/zapojse/')
    html = extract_issues_html(response.get_data(as_text=True))

    assertions = [
        ('Test Issue', 'Issue title'),
        ('http://github.com/pyvec/zapojse/issues/42', 'Issue URL'),
        ('https://github.com/encukou', 'Issue author URL'),
        ('od encukou', 'Issue author'),
        ('komentářů: 5', 'Comments count'),
        ('účastníků diskuze: 6', 'Participants count'),
        ('hlasů: 3', 'Votes count'),
    ]
    assert response.status_code == 200
    for expectation, description in assertions:
        assert expectation in html, description + " isn't present in the HTML"


@pytest.mark.parametrize('label_name,label_text', [
    ('coach', 'Kouč pomůže!'),
    ('sprint-idea', 'Sprint'),
])
def test_get_involved_cs_renders_special_labels(github, test_client,
                                                label_name, label_text):
    """
    Some GitHub issue labels have a special meaning and the 'get_involved_cs'
    page promotes them
    """
    def get_issues(self, *args, **kwargs):
        return [generate_issue_mock(**{
            'labels': [label_name],
            label_name: True,
        })]
    github.get_issues = get_issues

    response = test_client.get('/zapojse/')
    html = extract_issues_html(response.get_data(as_text=True))

    assert response.status_code == 200
    assert label_text in html, "Special label isn't present in the HTML"


@pytest.mark.parametrize('repo_name,is_rendered,label_cls', [
    ('pyvec/zapojse', False, None),
    ('pyvec/repo', True, None),
    ('pyladiescz/repo', True, 'label-pyladies'),
])
def test_get_involved_cs_renders_repo_name(github, test_client,
                                           repo_name, is_rendered, label_cls):
    """
    If the issue (or pull request) is not from the pyvec/zapojse repository,
    it is preceeded by a link to its repository. If the issue is from the
    PyLadiesCZ GitHub organization, it is labeled with a 'PyLadies' label
    """
    def get_issues(self, *args, **kwargs):
        return [generate_issue_mock(
            html_url='http://github.com/{}/issues/42'.format(repo_name),
            repository_name=repo_name.split('/')[1],
            repository_url_html='http://github.com/{}/'.format(repo_name),
            organization_name=repo_name.split('/')[0],
        )]
    github.get_issues = get_issues

    response = test_client.get('/zapojse/')
    html = extract_issues_html(response.get_data(as_text=True))

    if is_rendered:
        assert 'fa-code-fork' in html, "Repo icon isn't present in the HTML"
        url = 'http://github.com/{}/'.format(repo_name)
        assert url in html, "Repo URL isn't present in the HTML"
    else:
        assert 'fa-code-fork' not in html, "Repo icon is present in the HTML"
    if label_cls:
        assert label_cls in html, "Label isn't present in the HTML"


@pytest.mark.parametrize('is_pull_request,icon_name', [
    (True, 'fa-pencil-square'),
    (False, 'fa-exclamation-circle'),
])
def test_get_involved_cs_pull_request_icon(github, test_client,
                                           is_pull_request, icon_name):
    """
    Pull Requests have a different icon than Issues
    """
    def get_issues(self, *args, **kwargs):
        return [generate_issue_mock(is_pull_request=is_pull_request)]
    github.get_issues = get_issues

    response = test_client.get('/zapojse/')
    html = extract_issues_html(response.get_data(as_text=True))

    assert icon_name in html


def test_get_involved_cs_handles_error(github, test_client):
    """
    If error happens when generating the 'get_involved_cs' page, the view
    should handle it and still display most of the content. The issues
    section should contain an error message with some useful links
    """
    def get_issues(self, *args, **kwargs):
        raise RuntimeError('Ouch!')
    github.get_issues = get_issues

    response = test_client.get('/zapojse/')
    html = extract_issues_html(response.get_data(as_text=True))

    assert response.status_code == 500
    message = "DIV with the 'issues-error' class isn't present in the HTML"
    assert 'issues-error' in html, message
    message = "Link to alternative issues listing isn't present in the HTML"
    assert 'https://github.com/pyvec/zapojse/issues' in html, message
    url = '{base_url}?title={title}&amp;body={body}'.format(
        base_url='https://github.com/pyvec/python.cz/issues/new',
        title=url_quote_plus('Nefunguje Zapoj se'),
        body=url_quote_plus('RuntimeError: Ouch!'),
    )
    assert url in html, "URL for filing a bug report isn't present in the HTML"


def test_index_en_legacy_redirect(test_client):
    response = test_client.get('/english.html')
    url = url_for('index_en')
    html = response.get_data(as_text=True)
    head = html[:html.find('</head>')]
    assert '<meta http-equiv="refresh" content="0; {}">'.format(url) in head


@pytest.mark.parametrize('suffix', ('', 's001-install/'))
def test_pyladies_redirect(test_client, suffix):
    response = test_client.get('/pyladies/' + suffix)
    url = 'http://pyladies.cz/'
    if suffix:
        url += 'v1/' + suffix
    html = response.get_data(as_text=True)
    head = html[:html.find('</head>')]
    assert '<meta http-equiv="refresh" content="0; {}">'.format(url) in head


def test_talks_pdf_download(test_client):
    response = test_client.get(
        '/talks/brno-2013-11-28-veros-kaplan-postgis.pdf'
    )
    assert response.headers['content-type'] == 'application/pdf'
