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
        issues = []
        for org_name in org_names:
            for issue in _get_issues_for_org(org_name):
                issues.append(_enhance_issue(issue))
        issues = sorted(issues, key=_get_issue_sort_key, reverse=True)
        cache.set('github-issues', issues)
    return issues


def _get_issues_for_org(org_name):
    now = datetime.now()
    user_agent = ('pythoncz/{now.year}-{now.month} '
                  '(+http://python.cz)').format(now=now)

    session = requests.Session()
    session.headers.update({
        'User-Agent': user_agent,
        'Authorization': 'token {}'.format(app.config['GITHUB_TOKEN']),
    })

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


def _enhance_issue(issue):
    repo_url_segments = issue['repository_url'].split('/')
    repo_full_name = '{}/{}'.format(
        repo_url_segments[-2],
        repo_url_segments[-1]
    )

    issue['repository_name'] = repo_url_segments[-1]
    issue['organization_name'] = repo_url_segments[-2]
    issue['repository_full_name'] = repo_full_name
    issue['repository_url_html'] = 'https://github.com/' + repo_full_name

    return issue


def _get_issue_sort_key(issue):
    return issue.get('updated_at')
