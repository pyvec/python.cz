import re
import warnings

import pytest
import requests
import responses
from werkzeug.contrib.cache import NullCache

from pythoncz.models import github as github_module
from pythoncz_tests.models import github_test_fixtures as fixtures


class RequestsMock(responses.RequestsMock):
    def add_github_graphql(self, *args, **kwargs):
        """
        Convenience method to simplify adding fake responses for calls
        to GitHub's v4 GraphQL API
        """
        return self.add(responses.POST, 'https://api.github.com/graphql',
                        *args, **kwargs)


@pytest.fixture()
def requests_mock():
    """Provides mechanism for faking HTTP responses"""
    with RequestsMock() as mock:
        yield mock


@pytest.fixture()
def github():
    """Provides the 'github' module with caching disabled"""
    original_cache = github_module.cache
    github_module.cache = NullCache()
    yield github_module
    github_module.cache = original_cache


def test_get_issues_merges_orgs(github, requests_mock):
    """
    Tests whether 'get_issues' makes two HTTP requests for each given GitHub
    organization name and whether both data gets combined in the results
    """
    issue_org1 = fixtures.issue()
    requests_mock.add_github_graphql(
        json=fixtures.api_response_body(repos=[
            fixtures.repository(issues=[issue_org1], pull_requests=[],
                                private=False),
        ]),
    )
    issue_org2 = fixtures.issue()
    requests_mock.add_github_graphql(
        json=fixtures.api_response_body(repos=[
            fixtures.repository(issues=[issue_org2], pull_requests=[],
                                private=False),
        ]),
    )

    issues = github.get_issues(['org1', 'org2'])
    titles = set(i['title'] for i in issues)

    assert titles == {issue_org1['title'], issue_org2['title']}


def test_get_issues_api_error(github, requests_mock):
    """
    In case of API error, the 'get_issues' function should raise HTTPError
    with combined error messages
    """
    requests_mock.add_github_graphql(
        status=500,
        json={'errors': [{'message': 'Error 1'}, {'message': 'Error 2'}]},
    )
    error_message = 'Error 1; Error 2'
    with pytest.raises(requests.HTTPError, match=error_message) as excinfo:
        github.get_issues(['org'])

    assert excinfo.value.response.status_code == 500


def test_create_api_session(github):
    """
    The '_create_api_session' helper should add User-Agent and Authorization
    HTTP headers to the HTTP session
    """
    session = github._create_api_session()
    headers = session.headers

    assert 'https://python.cz' in headers.get('User-Agent')
    assert re.match(r'token \w+', headers.get('Authorization'))


def test_get_issues_for_org_key_error(github, requests_mock):
    """
    If the API response doesn't have the expected structure, the
    '_get_issues_for_org' helper should raise ValueError
    """
    requests_mock.add_github_graphql(json={'data': {}})
    error_message = 'Unexpected structure of the GitHub API response'
    with pytest.raises(ValueError, message=error_message):
        list(github._get_issues_for_org(requests.Session(), 'org'))


def test_get_issues_for_org_merges_issues_pull_requests(github, requests_mock):
    """
    The '_get_issues_for_org' helper should merge both issues with
    pull requests and treat them both as issues
    """
    repo1 = fixtures.repository(
        issues=[fixtures.issue(), fixtures.issue(), fixtures.issue()],
        pull_requests=[fixtures.issue(pr=True)],
        private=False
    )
    repo2 = fixtures.repository(
        issues=[fixtures.issue(), fixtures.issue()],
        pull_requests=[fixtures.issue(pr=True), fixtures.issue(pr=True)],
        private=False
    )

    expected_titles_are_pr = {}
    for repo in [repo1, repo2]:
        for issue in repo['issues']['nodes']:
            expected_titles_are_pr[issue['title']] = False
        for pull_request in repo['pullRequests']['nodes']:
            expected_titles_are_pr[pull_request['title']] = True

    api_response_body = fixtures.api_response_body(repos=[repo1, repo2])
    requests_mock.add_github_graphql(json=api_response_body)
    issues = github._get_issues_for_org(requests.Session(), 'org')

    titles_are_pr = {i['title']: i['is_pull_request'] for i in issues}

    assert titles_are_pr == expected_titles_are_pr


def test_get_issues_for_org_skips_private(github, requests_mock):
    """
    The '_get_issues_for_org' helper should skip private repositories
    """
    public_repo = fixtures.repository(private=False)

    expected_titles = set()
    for issue in public_repo['issues']['nodes']:
        expected_titles.add(issue['title'])
    for pull_request in public_repo['pullRequests']['nodes']:
        expected_titles.add(pull_request['title'])

    api_response_body = fixtures.api_response_body(repos=[
        fixtures.repository(private=True),
        public_repo,
        fixtures.repository(private=True),
        fixtures.repository(private=True),
        fixtures.repository(private=True),
    ])
    requests_mock.add_github_graphql(json=api_response_body)
    issues = github._get_issues_for_org(requests.Session(), 'org')

    titles = set(i['title'] for i in issues)
    assert titles == expected_titles


def test_request_api_200_invalid_json(github, requests_mock):
    """
    The '_request_api' helper should raise 'ValueError' if the JSON in the
    response cannot be decoded
    """
    requests_mock.add_github_graphql(body='... invalid JSON ...')
    error_message = 'Unexpected structure of the GitHub API response'
    with pytest.raises(ValueError, message=error_message):
        github._request_api(requests.Session(), '... query ...', {})


def test_request_api_500_invalid_json(github, requests_mock):
    """
    The '_request_api' helper should raise HTTP error even if the JSON in the
    response cannot be decoded
    """
    requests_mock.add_github_graphql(status=500, body='... invalid JSON ...')
    with pytest.raises(requests.HTTPError) as excinfo:
        github._request_api(requests.Session(), '... query ...', {})

    assert excinfo.value.response.status_code == 500


@pytest.mark.parametrize('status_code', (200, 500))
def test_request_api_X00_errors(github, requests_mock, status_code):
    """
    The '_request_api' helper should raise HTTP error with error messages
    sent in the response body if they're present, regardless of the HTTP status
    code
    """
    requests_mock.add_github_graphql(
        status=status_code,
        json={'errors': [{'message': 'Error 1'}, {'message': 'Error 2'}]},
    )
    error_message = 'Error 1; Error 2'
    with pytest.raises(requests.HTTPError, match=error_message) as excinfo:
        github._request_api(requests.Session(), '... query ...', {})

    assert excinfo.value.response.status_code == status_code


def test_request_api_200(github, requests_mock):
    """
    The '_request_api' helper should parse valid JSON response and return it
    """
    requests_mock.add_github_graphql(json={'data': '...'})
    json = github._request_api(requests.Session(), '... query ...', {})

    assert json == {'data': '...'}


def test_request_api_500(github, requests_mock):
    """
    The '_request_api' helper should raise HTTP error if the HTTP status code
    indicates HTTP error, even if there are no errors in the JSON response
    """
    requests_mock.add_github_graphql(status=500, json={'data': '...'})
    with pytest.raises(requests.HTTPError) as excinfo:
        github._request_api(requests.Session(), '... query ...', {})

    assert excinfo.value.response.status_code == 500


def test_format_issue_missing_author(github):
    """
    The '_format_issue' helper should be able to deal with the situation
    when the author is deleted/disabled user
    """
    issue = fixtures.issue()
    issue['author'] = None
    formatted_issue = github._format_issue('org', fixtures.repository(), issue)

    assert formatted_issue['user'] == {
        'login': None,
        'html_url': 'https://github.com/ghost',
    }


def test_format_issue_labels(github):
    """The '_format_issue' helper should be able to process labels"""
    issue = fixtures.issue(labels=[{'name': 'bug'}, {'name': 'feature'}])
    formatted_issue = github._format_issue('org', fixtures.repository(), issue)

    assert formatted_issue['labels'] == ['bug', 'feature']
    assert formatted_issue['coach'] is False


@pytest.mark.parametrize('label_name', ('coach', 'sprint-idea'))
def test_format_issue_special_labels(github, label_name):
    """
    The '_format_issue' helper should be able to process the 'coach' label
    and to mark the resulting formatted issue with the 'coach' flag accordingly
    """
    issue = fixtures.issue(labels=[{'name': 'bug'}, {'name': label_name}])
    formatted_issue = github._format_issue('org', fixtures.repository(), issue)

    assert formatted_issue['labels'] == ['bug', label_name]
    assert formatted_issue[label_name] is True


def test_format_issue_reactions(github):
    """
    The '_format_issue' helper should be able to calculate 'votes'
    from reactions
    """
    issue = fixtures.issue(reactions_counts={
        'LAUGH': 42,
        'HEART': 3,
    })
    formatted_issue = github._format_issue('org', fixtures.repository(), issue)

    assert formatted_issue['votes'] == 42 + 3


def test_calculate_votes(github):
    """
    The '_calculate_votes' helper should correctly deal with negative votes
    """
    votes = github._calculate_votes(fixtures.issue(reactions_counts={
        'THUMBS_UP': 1,
        'THUMBS_DOWN': 1,
        'LAUGH': 1,
        'HOORAY': 1,
        'CONFUSED': 1,
        'HEART': 1,
    }))

    assert votes == 2


def test_get_nodes_without_total_count(github):
    subnodes = [1, 2, 3, 4]
    result = github._get_nodes({'something': {'nodes': subnodes}}, 'something')

    assert result == subnodes


def test_get_nodes_with_total_count(github):
    subnodes = [1, 2, 3, 4]
    result = github._get_nodes({'something': {
        'totalCount': len(subnodes),
        'nodes': subnodes,
    }}, 'something')

    assert result == subnodes


def test_get_nodes_with_different_total_count(github):
    """
    If the total count of sub-nodes is different then the number of sub-nodes
    available in the API response, at least warn about the fact that there's
    some data missing and limits should be raised or results paginated
    """
    subnodes = [1, 2, 3, 4]
    node = {'something': {
        'totalCount': len(subnodes) + 42,
        'nodes': subnodes,
    }}
    with warnings.catch_warnings(record=True) as recorded_warnings:
        result = github._get_nodes(node, 'something')

    assert result == subnodes
    assert len(recorded_warnings) == 1
    assert issubclass(recorded_warnings[0].category, UserWarning)
    assert 'nodes in total, but only' in str(recorded_warnings[0].message)


def test_sort_issues_coach(github):
    """
    Issues with coaching offer should always go first no matter what
    """
    repository = fixtures.repository()
    issues = [github._format_issue('org', repository, issue) for issue in [
        fixtures.issue(labels=[]),
        fixtures.issue(labels=[{'name': 'foo'}]),
        fixtures.issue(labels=[{'name': 'bar'}, {'name': 'coach'}]),
        fixtures.issue(labels=[]),
    ]]
    sorted_issues = github._sort_issues(issues)

    assert sorted_issues[0]['coach'] is True


def test_sort_issues_votes(github):
    """
    Issues with most votes should go first if there's no 'coach' issue
    """
    repository = fixtures.repository()
    issues = [github._format_issue('org', repository, issue) for issue in [
        fixtures.issue(labels=[], reactions_counts={'THUMBS_UP': 1}),
        fixtures.issue(labels=[], reactions_counts={'THUMBS_DOWN': 1}),
        fixtures.issue(labels=[], reactions_counts={'THUMBS_UP': 4}),
        fixtures.issue(labels=[], reactions_counts={'THUMBS_UP': 3}),
    ]]
    sorted_issues = github._sort_issues(issues)

    assert sorted_issues[0]['votes'] == 4


def test_sort_issues_activity(github):
    """
    Issues with most user activity should go first if there's no 'coach'
    issue and no reactions.
    User activity is comments count + participants count
    """
    issue1 = fixtures.issue(labels=[], reactions_counts={})
    issue1['comments']['totalCount'] = 3
    issue1['participants']['totalCount'] = 2

    issue2 = fixtures.issue(labels=[], reactions_counts={})
    issue2['comments']['totalCount'] = 1
    issue2['participants']['totalCount'] = 9

    issue3 = fixtures.issue(labels=[], reactions_counts={})
    issue3['comments']['totalCount'] = 0
    issue3['participants']['totalCount'] = 4

    repository = fixtures.repository()
    sorted_issues = github._sort_issues([
        github._format_issue('org', repository, issue)
        for issue in [issue1, issue2, issue3]
    ])

    assert sorted_issues[0]['comments'] == 1  # + 9 = 10
    assert sorted_issues[1]['comments'] == 3  # + 2 = 7
    assert sorted_issues[2]['comments'] == 0  # + 4 = 4
