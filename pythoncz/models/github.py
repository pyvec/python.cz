# -*- coding: utf-8 -*-


from datetime import datetime

import requests
from werkzeug.contrib.cache import FileSystemCache

from .. import app


__all__ = ('get_issues',)


cache = FileSystemCache(app.config['CACHE_DIR'], default_timeout=3600)


def get_issues(org_names):
    issues = cache.get('github-issues')
    if issues is None:
        session = _create_github_api_session()
        issues = []
        for org_name in org_names:
            for issue in _get_issues_for_org(session, org_name):
                issues.append(_enhance_issue(session, issue))
        issues = sorted(issues, key=_get_issue_sort_key, reverse=True)
        cache.set('github-issues', issues)
    return issues


def _create_github_api_session():
    now = datetime.now()
    user_agent = ('pythoncz/{now.year}-{now.month} '
                  '(+https://python.cz)').format(now=now)

    session = requests.Session()
    session.headers.update({
        'User-Agent': user_agent,
        'Authorization': 'token {}'.format(app.config['GITHUB_TOKEN']),
        'Accept': 'application/vnd.github.squirrel-girl-preview',
    })
    return session


def _get_issues_for_org(session, org_name):
    search_conditions = [
        'is:open',
        'is:issue',
        'org:{}'.format(org_name)
    ]

    page = 1
    while True:
        res = session.get('https://api.github.com/search/issues', params={
            'q': ' '.join(search_conditions),
            'per_page': 100,
            'page': page,
        })
        res.raise_for_status()
        items = res.json().get('items', [])
        if items:
            yield from items
            page += 1
        else:
            break


def _enhance_issue(session, issue):
    repo_url_segments = issue['repository_url'].split('/')
    repo_full_name = '{}/{}'.format(
        repo_url_segments[-2],
        repo_url_segments[-1]
    )

    res = session.get('https://api.github.com/repos/{}/issues/{}'.format(
        repo_full_name,
        issue['number']
    ))
    res.raise_for_status()
    issue_details = res.json()

    try:
        reactions = issue_details['reactions']
        issue['votes'] = (
            reactions.get('total_count', 0)
            - reactions.get('-1', 0)
            - reactions.get('confused', 0)
        )
    except KeyError:
        issue['votes'] = 0

    issue['repository_name'] = repo_url_segments[-1]
    issue['organization_name'] = repo_url_segments[-2]
    issue['repository_full_name'] = repo_full_name
    issue['repository_url_html'] = 'https://github.com/' + repo_full_name

    return issue


def _get_issue_sort_key(issue):
    return (issue.get('votes'), issue.get('updated_at'))
