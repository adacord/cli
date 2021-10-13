import pytest

from adacord.cli.api import AdacordApi, HTTPClient, AccessTokenAuth


@pytest.fixture
def fake_token_getter():
    def token_getter():
        return "test"

    return token_getter


@pytest.fixture
def access_token_auth(fake_token_getter) -> AccessTokenAuth:
    return AccessTokenAuth(fake_token_getter)


@pytest.fixture
def http_client(access_token_auth) -> HTTPClient:
    return HTTPClient(auth=access_token_auth)


@pytest.fixture
def api(http_client) -> AdacordApi:
    yield AdacordApi(client=http_client)
