
import pytest
import requests
import requests_mock
from requests import Request
from requests.auth import AuthBase

from adacord.cli.api import (AccessTokenAuth, CustomHTTPAdapter, HTTPClient,ApiClient, AdacrdClient, AdacordApi)
from adacord.cli.exceptions import AdacordApiError


@pytest.fixture
def fake_token_getter():
    def token_getter():
        return 'test'
    return token_getter


@pytest.fixture
def access_token_auth(fake_token_getter) -> AccessTokenAuth:
    return AccessTokenAuth(fake_token_getter)


class TestAccessTokenAuth:

    def test_init(self, fake_token_getter):
        token_getter = AccessTokenAuth(fake_token_getter)
        assert token_getter
        assert isinstance(token_getter, AuthBase)

    def test_get_token(self, access_token_auth):
        result = access_token_auth.get_token()
        assert result == 'test'

    def test__call__(self, access_token_auth):
        fake_request = Request()

        access_token_auth(fake_request)

        assert fake_request.headers["Authorization"] == "Bearer test"

class TestCustomHTTPAdapter:

    def test_init(self):
        adapter = CustomHTTPAdapter()
        assert adapter
        assert isinstance(adapter, requests.adapters.HTTPAdapter)


@pytest.fixture
def http_client(access_token_auth) -> HTTPClient:
    return HTTPClient(auth=access_token_auth)


class TestHTTPClient:
    def test_init(self, access_token_auth):
        http_client = HTTPClient(auth=access_token_auth)
        assert http_client
        assert isinstance(http_client, requests.Session)

    def test_with_token(self):
        http_client = HTTPClient.with_token(token='1234')
        assert http_client
        assert isinstance(http_client, requests.Session)
        assert http_client.auth.get_token() == '1234'

    def test_request(self, http_client):
        with requests_mock.Mocker() as mock:
            mock.get('https://tururu.com', json={'hello': 'world'}, status_code=200)
            response = http_client.request('GET', 'https://tururu.com')
            assert response.ok
            assert response.json() == {'hello': 'world'}

    def test_request_raises(self, http_client):
        with requests_mock.Mocker() as mock:
            mock.get('https://tururu.com', json={'error': 'not found'}, status_code=404)
            with pytest.raises(AdacordApiError):
                http_client.request('GET', 'https://tururu.com')

class TestApiClient:

    def test_init(self, http_client):
        api_client = ApiClient(client=http_client)
        assert api_client
        assert api_client.client == http_client

    def test_base_path(self, http_client):
        api_client = ApiClient(client=http_client)
        assert api_client.base_path == "https://api.adacord.com"

    def test_url_for(self, http_client):
        api_client = ApiClient(client=http_client)
        result = api_client.url_for("/test")
        assert result == "https://api.adacord.com/v1/test"

class TestAdacrdClient:
    def test_init(self, http_client):
        api_client = AdacrdClient(bucket_name='dump', client=http_client)
        assert api_client
        assert api_client.client == http_client
        assert api_client.bucket_name == 'dump'

    def test_base_path(self, http_client):
        api_client = AdacrdClient(bucket_name='dump', client=http_client)
        assert api_client.base_path == "https://dump.adacrd.in"

    def test_url_for(self, http_client):
        api_client = AdacrdClient(bucket_name='dump', client=http_client)
        result = api_client.url_for("/test")
        assert result == "https://dump.adacrd.in/v1/test"

# class TestUser:
#     def test_user__create(self, requests_mock, api):
#         data = {
#             "uid": "123456",
#             "display_name": "fake user",
#             "email": "fake@adacord.com",
#             "phone_number": "+123456",
#             "photo_url": "https+fake://test.photo.here",
#             "email_verified": "false",
#         }
#         requests_mock.post("http://fake.example:8000/v1/users", json=data)
#         api.user.create("email", "password")

#     def test_user__login(self, requests_mock, api):
#         data = {
#             "access_token": "",
#             "refresh_token": "",
#             "user_email": "",
#             "expires_in": "",
#         }
#         requests_mock.post(
#             "http://fake.example:8000/v1/users/token", json=data
#         )
#         response = api.user.login("email", "password")
#         assert response


# class TestBucket:
#     def test_bucket__create(self, requests_mock, api):
#         data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.post("http://fake.example:8000/v1/buckets", json=data)
#         response = api.bucket.create("my-bucket", schemaless=False)
#         assert response == data

#     def test_bucket__get_all(self, requests_mock, api):
#         data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.get("http://fake.example:8000/v1/buckets", json=data)
#         response = api.bucket.get()
#         assert response

#     def test_bucket_get_single(self, requests_mock, api):
#         data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.get(
#             "http://fake.example:8000/v1/buckets/my-bucket", json=data
#         )
#         response = api.bucket.get("my-bucket")
#         assert response

#     def test_bucket__delete(self, requests_mock, api):
#         data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.delete(
#             "http://fake.example:8000/v1/buckets/email", json=data
#         )
#         response = api.bucket.delete("email")
#         assert response

#     def test_bucket__webhook_create(self, requests_mock, api):
#         data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.post(
#             "http://fake.example:8000/v1/buckets/my-bucket/webhooks", json=data
#         )
#         response = api.bucket.create_webhook(
#             "my-bucket",
#             "select * from my-bucket",
#             "https://my-webhook-url.com",
#         )
#         assert response


# class TestAdacrd:
#     def test_adacrd__query(self, requests_mock, api):
#         data = {"query": "", "result": []}
#         # data = {
#         #     "description": "",
#         #     "data_schema": {},
#         # }
#         requests_mock.post(
#             "http://fake.example:8000/v1/buckets/email/query", json=data
#         )
#         response = api.bucket.query("email", "select * from my-bucket")
#         assert response
