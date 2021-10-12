import pytest

from adacord.cli.api import AccessTokenAuth, HTTPClient, ApiClient, AdacrdClient, AdacordApi


@pytest.fixture
def api():
    token_getter = (
        lambda: "fake-token"
    )  # noqa: E731 do not assign a lambda expression
    http_client = HTTPClient(auth=AccessTokenAuth(token_getter))
    yield AdacordApi(client=http_client)
