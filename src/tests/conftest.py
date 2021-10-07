import pytest

from cli.api import Client, AdacordApi, AccessTokenAuth


@pytest.fixture
def api():
    token_getter = lambda: "fake-token"
    client = Client(
        base_path="http://fake.example:8000/v1",
        auth=AccessTokenAuth(token_getter),
    )
    yield AdacordApi(client)
