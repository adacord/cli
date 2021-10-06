import pytest

from adacord.cli.api import Client, AdacordApi


@pytest.fixture
def api():
    yield AdacordApi(Client(get_token=lambda: "fake-token"))
