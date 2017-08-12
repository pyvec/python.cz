import os
import itertools
import warnings
from datetime import datetime

import requests
from werkzeug.contrib.cache import FileSystemCache

from .. import app


__all__ = ('get_issues',)


get_issues_graphql_filename = (
    os.path.join(os.path.dirname(__file__), 'github_get_issues.graphql')
)
with open(get_issues_graphql_filename) as f:
    GET_ISSUES_GRAPHQL = f.read()

SIX_HOURS_AS_SECONDS = 21600


cache = FileSystemCache(app.config['CACHE_DIR'],
                        default_timeout=SIX_HOURS_AS_SECONDS)


def get_issues(org_names):
    issues = cache.get('github-issues')
    if issues is None:
        session = _create_github_api_session()
        issues = itertools.chain(*(
            _get_issues_for_org(session, org_name) for org_name in org_names)
        )
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
    })
    return session


def _get_issues_for_org(session, org_name):
    res = session.post('https://api.github.com/graphql', json={
        'query': GET_ISSUES_GRAPHQL,
        'variables': {'org_name': org_name}
    })
    res.raise_for_status()

    json = res.json()
    if json.get('errors'):
        message = '. '.join(error['message'] for error in json['errors'])
        raise requests.RequestException(message)

    try:
        organization = json['data']['organization']
        repositories = _get_nodes(organization, 'repositories')

        for repository in repositories:
            if repository['isPrivate']:
                continue

            for issue in _get_nodes(repository, 'issues'):
                yield _format_issue(org_name, repository, issue)

            for pull_request in _get_nodes(repository, 'pullRequests'):
                yield _format_issue(org_name, repository, pull_request,
                                    is_pull_request=True)
    except KeyError as e:
        raise ValueError(
            'Unexpected structure of the GitHub API response: {}'.format(e)
        )


def _format_issue(org_name, repository, issue, is_pull_request=False):
    author = issue['author'] or {
        'login': None,
        'url': 'https://github.com/ghost',
    }
    labels = [label['name'] for label in _get_nodes(issue, 'labels')]

    return {
        'title': issue['title'],
        'html_url': issue['url'],
        'updated_at': issue['updatedAt'],
        'user': {
            'login': author['login'],
            'html_url': author['url'],
        },
        'is_pull_request': is_pull_request,
        'repository_name': repository['name'],
        'repository_url_html': repository['url'],
        'organization_name': org_name,
        'comments': issue['comments']['totalCount'],
        'participants': issue['participants']['totalCount'],
        'votes': _get_reactions(issue),
        'labels': labels,
        'coach': 'coach' in labels,
    }


def _get_reactions(issue):
    votes = 0
    for reaction in _get_nodes(issue, 'reactions'):
        if reaction['content'] in ['THUMBS_DOWN', 'CONFUSED']:
            votes -= 1
        else:
            votes += 1
    return votes


def _get_nodes(node, connection_name):
    connection_nodes = node[connection_name]['nodes']

    if 'totalCount' in node[connection_name]:
        connection_nodes_count = len(connection_nodes)
        connection_nodes_total_count = node[connection_name]['totalCount']

        if connection_nodes_count > connection_nodes_total_count:
            warnings.warn((
                "The '{}' contain {} nodes in total, but only {} was fetched"
            ).format(
                connection_name,
                connection_nodes_total_count,
                connection_nodes_count,
            ), warnings.UserWarning)

    return connection_nodes


def _get_issue_sort_key(issue):
    return (
        not issue.get('assignee'),
        issue.get('coach'),
        issue.get('votes'),
        issue.get('comments'),
        issue.get('updated_at'),
    )
