# -*- coding: utf-8 -*-


import itertools
from datetime import datetime

import requests
import grequests
from werkzeug.contrib.cache import FileSystemCache

from .. import app


__all__ = ('get_issues',)


cache = FileSystemCache(app.config['CACHE_DIR'], default_timeout=3600)


def get_issues(org_names):
    issues = cache.get('github-issues')
    if issues is None:
        session = _create_github_api_session()
        issues = itertools.chain(*(_get_issues_for_org(session, org)
                                   for org in org_names))
        # Using grequests here to get the issues details asynchronously
        # Note that it does not support session, so we set the headers manually
        reqs = (grequests.get(_issue_url(issue), headers=session.headers)
                for issue in issues)
        issues = [_enhance_issue(response) for response in grequests.map(reqs)]
        issues = sorted(issues, key=_get_issue_sort_key, reverse=True)
        cache.set('github-issues', issues)
    return issues


def _create_github_api_session():
    user_agent = ('pythoncz/{now.year}-{now.month} '
                  '(+https://python.cz)').format(now=datetime.now())

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


def _issue_repo_slug(issue):
    repo_url_segments = issue['repository_url'].split('/')
    org, repo = repo_url_segments[-2], repo_url_segments[-1]
    return org, repo, '{}/{}'.format(org, repo)


def _issue_url(issue):
    org, repo, slug = _issue_repo_slug(issue)
    return 'https://api.github.com/repos/{}/issues/{}'.format(
        slug,
        issue['number']
    )


def _enhance_issue(res):
    res.raise_for_status()
    issue = res.json()

    try:
        is_pull_request = bool(issue['pull_request']['url'])
    except KeyError:
        is_pull_request = False

    try:
        reactions = issue['reactions']
        issue['votes'] = (
            reactions.get('total_count', 0)
            - reactions.get('-1', 0)
            - reactions.get('confused', 0)
        )
    except KeyError:
        issue['votes'] = 0

    labels = [label['name'] for label in issue.get('labels', [])]

    org, repo, slug = _issue_repo_slug(issue)

    issue['coach'] = 'coach' in labels
    issue['is_pull_request'] = is_pull_request
    issue['repository_name'] = repo
    issue['organization_name'] = org
    issue['repository_full_name'] = slug
    issue['repository_url_html'] = 'https://github.com/' + slug

    return issue


def _get_issue_sort_key(issue):
    return (
        not issue.get('assignee'),
        issue.get('coach'),
        issue.get('votes'),
        issue.get('comments'),
        issue.get('updated_at'),
    )
