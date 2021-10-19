import pytest
import requests_mock

from adacord.cli.api import Bucket, AdacordApi, HTTPClient, AccessTokenAuth


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


@pytest.fixture
def bucket_client(api, fake_bucket_data) -> Bucket:
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://api.adacord.com/v1/buckets/123", json=fake_bucket_data
        )
        client = api.Bucket("123")
        yield client


@pytest.fixture
def fake_token_data():
    return {
        "uuid": "8901",
        "created_on": {},
        "token": "tEsTtOkEn",
        "description": "",
    }


@pytest.fixture
def fake_bucket_data():
    return {
        "uuid": "123",
        "name": "buckety",
        "url": "https://your-bucket.ada.in",
        "schemaless": "false",
        "description": "fake bucket",
    }
