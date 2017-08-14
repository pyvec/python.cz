import uuid
import random


def api_response_body(repos=None, repos_count=None):
    if repos is None:
        if repos_count is None:
            repos_count = random.randint(2, 4)
        repos = [repository() for i in range(repos_count)]
    else:
        repos_count = len(repos)

    return {'data': {'organization': {'repositories': {
        'totalCount': repos_count,
        'nodes': repos,
    }}}}


def repository(issues=None, issues_count=None,
               pull_requests=None, pull_requests_count=None,
               private=None):
    if issues is None:
        if issues_count is None:
            issues_count = random.randint(0, 4)
        issues = [issue() for i in range(issues_count)]
    else:
        issues_count = len(issues)

    if pull_requests is None:
        if pull_requests_count is None:
            pull_requests_count = random.randint(0, 4)
        pull_requests = [
            issue(pr=True) for i in range(pull_requests_count)
        ]
    else:
        pull_requests_count = len(pull_requests)

    if private is None:
        private = random.choice([True, False])

    return {
        'name': 'repo-{}'.format(uuid.uuid4()),
        'nameWithOwner': 'org/repo',
        'isPrivate': private,
        'url': 'https://github.com/org/repo',
        'issues': {
            'totalCount': issues_count,
            'nodes': issues,
        },
        'pullRequests': {
            'totalCount': pull_requests_count,
            'nodes': pull_requests,
        },
    }


def issue(pr=False, labels=None, reactions_counts=None):
    issue_number = random.randint(1, 4242)
    author = random.choice(['zuzejk', 'zzuzzy', 'encukou', 'honzajavorek'])

    if pr:
        issue_type = 'pull'
        title = "Fix '{}'".format(uuid.uuid4())
    else:
        issue_type = 'issue'
        title = "Looks like '{}' is broken".format(uuid.uuid4())

    url = 'https://github.com/org/repo/{}/{}'.format(issue_type, issue_number)

    if labels is None:
        labels_fake_values = ['bug', 'improvement', 'coach', 'duplicate']
        labels_count = random.randint(0, len(labels_fake_values))
        labels = [
            {'name': label_name} for label_name in
            random.sample(labels_fake_values, labels_count)
        ]

    return {
        'title': title,
        'url': url,
        'updatedAt': '2017-02-07T16:52:01Z',
        'author': {
            'login': author,
            'url': 'https://github.com/{}'.format(author),
        },
        'labels': {'nodes': labels},
        'reactions': {'nodes': reactions(reactions_counts)},
        'comments': {'totalCount': random.randint(1, 4242)},
        'participants': {'totalCount': random.randint(1, 42)},
    }


def reactions(reactions_counts=None):
    if reactions_counts is None:
        reaction_types = random.sample([
            'THUMBS_UP', 'THUMBS_DOWN', 'LAUGH', 'HOORAY', 'CONFUSED', 'HEART'
        ], random.randint(0, 6))
        reactions_counts = {}
        for reaction_type in reaction_types:
            reactions_counts[reaction_type] = random.randint(1, 42)
    if reactions_counts:
        reactions = []
        for reaction_type, count in reactions_counts.items():
            for i in range(count):
                reactions.append({'content': reaction_type})
        return reactions
    return []
