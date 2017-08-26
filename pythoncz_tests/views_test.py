import pytest
from flask import url_for

from pythoncz import app


@pytest.fixture
def test_client():
    app.testing = True
    with app.test_client() as client:
        yield client
    app.testing = False


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
