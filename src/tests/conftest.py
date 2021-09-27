import pytest

from cli.api import AdacordApi, Client


@pytest.fixture
def api():
    yield AdacordApi(Client(get_token=lambda: "fake-token"))
