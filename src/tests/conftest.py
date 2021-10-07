import pytest

from adacord.cli.api import Client, AdacordApi, AccessTokenAuth


@pytest.fixture
def api():
    token_getter = (
        lambda: "fake-token"
    )  # noqa: E731 do not assign a lambda expression
    client = Client(
        base_path="http://fake.example:8000/v1",
        auth=AccessTokenAuth(token_getter),
    )
    yield AdacordApi(client)
