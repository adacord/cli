import json

import pytest
import requests
import requests_mock
from requests import Request
from requests.auth import AuthBase

from adacord.cli.api import (
    ApiClient,
    AdacordApi,
    BucketArgs,
    HTTPClient,
    AccessTokenAuth,
    CustomHTTPAdapter,
)
from adacord.cli.exceptions import AdacordApiError


class TestAccessTokenAuth:
    def test_init(self, fake_token_getter):
        token_getter = AccessTokenAuth(fake_token_getter)
        assert token_getter
        assert isinstance(token_getter, AuthBase)

    def test_get_token(self, access_token_auth):
        result = access_token_auth.get_token()
        assert result == "test"

    def test__call__(self, access_token_auth):
        fake_request = Request()

        access_token_auth(fake_request)

        assert fake_request.headers["Authorization"] == "Bearer test"


class TestCustomHTTPAdapter:
    def test_init(self):
        adapter = CustomHTTPAdapter()
        assert adapter
        assert isinstance(adapter, requests.adapters.HTTPAdapter)


class TestHTTPClient:
    def test_init(self, access_token_auth):
        http_client = HTTPClient(auth=access_token_auth)
        assert http_client
        assert isinstance(http_client, requests.Session)
        assert http_client.auth.get_token() == "test"

    def test_with_token(self):
        http_client = HTTPClient.with_token(token="1234")
        assert http_client
        assert isinstance(http_client, requests.Session)
        assert http_client.auth.get_token() == "1234"

    def test_request(self, http_client):
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://tururu.com", json={"hello": "world"}, status_code=200
            )
            response = http_client.request("GET", "https://tururu.com")
            assert response.ok
            assert response.json() == {"hello": "world"}

    def test_request_raises(self, http_client):
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://tururu.com",
                json={"error": "not found"},
                status_code=404,
            )
            with pytest.raises(AdacordApiError):
                http_client.request("GET", "https://tururu.com")

    def test_request_headers(self, http_client):
        def callback(request, context):
            assert "Authorization" in request.headers

        with requests_mock.Mocker() as m:
            m.get("https://tururu.com", text=callback)
            http_client.get("https://tururu.com")

    def test_request_headers_with_token(self, access_token_auth):
        http_client = HTTPClient(auth=access_token_auth)

        def callback(request, context):
            assert "Authorization" in request.headers

        with requests_mock.Mocker() as m:
            m.get("https://tururu.com", text=callback)
            http_client.get("https://tururu.com")


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
        assert result == "https://api.adacord.com/v0/test"


class TestUser:
    """Test the endpoints that deal with users"""

    def test_create(self, api):
        data = {
            "uid": "123456",
            "display_name": "fake user",
            "email": "fake@adacord.com",
            "phone_number": "+123456",
            "photo_url": "https+fake://test.photo.here",
            "email_verified": "false",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v0/users", json=data)
            api.User.create("email", "password")

    def test_login(self, api):
        data = {
            "access_token": "",
            "refresh_token": "",
            "user_email": "",
            "expires_in": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v0/users/token", json=data)
            response = api.User.login("email", "password")
            assert response

    def test_request_password_reset(self, api):
        data = {"message": "ok"}
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/users/password_reset", json=data
            )
            response = api.User.request_password_reset("email")
            assert response

    def test_request_verification_email(self, api):
        data = {"message": "ok"}
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/users/verification_email",
                json=data,
            )
            response = api.User.request_verification_email("email", "password")
            assert response


class TestBuckets:
    """Test API interface that deal with buckets"""

    def test_buckets__create(self, api, fake_bucket_data):
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/buckets", json=fake_bucket_data
            )
            bucket = api.Buckets.create("123", schemaless=False)
            assert bucket.uuid == fake_bucket_data["uuid"]
            assert bucket.name == fake_bucket_data["name"]
            assert bucket.url == fake_bucket_data["url"]
            assert bucket.description == fake_bucket_data["description"]

    def test_buckets__list(self, api, fake_bucket_data):
        data = [fake_bucket_data]
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v0/buckets", json=data)
            response = api.Buckets.list()
            assert response[0].uuid == data[0]["uuid"]
            assert response[0].name == data[0]["name"]
            assert response[0].url == data[0]["url"]
            assert response[0].description == data[0]["description"]

    def test_buckets__get(self, api, fake_bucket_data):
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v0/buckets/123", json=fake_bucket_data
            )
            response = api.Buckets.get("123")
            assert response

    def test_buckets__delete(self, api, fake_bucket_data):
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v0/buckets/123", json=fake_bucket_data
            )
            response = api.Buckets.delete("123")
            assert response

    def test_buckets__create_token(self, api, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/buckets/123/tokens",
                json=fake_token_data,
            )
            response = api.Buckets.create_token(bucket="123", description="")
            assert response == fake_token_data

    def test_buckets__get_tokens(self, api, fake_token_data):
        data = [fake_token_data]
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v0/buckets/123/tokens", json=data
            )
            response = api.Buckets.get_tokens(bucket="123")
            assert response == data

    def test_buckets__delete_token(self, api, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v0/buckets/123/tokens/8901",
                json=fake_token_data,
            )
            response = api.Buckets.delete_token(
                bucket="123", token_uuid="8901"
            )
            assert response == fake_token_data

    def test_buckets__query(self, api):
        data = {"query": "", "result": []}
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v0/buckets/query", json=data)
            response = api.Buckets.query("select * from my-bucket")
            assert response == data

    def test_buckets__push_data(self, api):
        rows = {"timestamp": "42", "data": []}
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v0/buckets/123/data", json=data)
            response = api.Buckets.push_data("123", rows)
            assert response == data

    def test_buckets__get_data(self, api):
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v0/buckets/123/data", json=data)
            response = api.Buckets.get_data("123")
            assert response == data


class TestBucket:
    """Test API interface that deals with a SINGLE bucket"""

    def test_bucket__get(self, api, fake_bucket_data):
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v0/buckets/123", json=fake_bucket_data
            )
            response = api.Bucket("123")
            assert response
            assert response.uuid
            assert response.name
            assert response.description
            assert response.url

    def test_bucket__delete(self, bucket_client):
        data = {"uuid": "123"}
        with requests_mock.Mocker() as mock:
            mock.delete("https://api.adacord.com/v0/buckets/123", json=data)
            response = bucket_client.delete()
            assert response == data

    def test_bucket__create_token(self, bucket_client, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/buckets/123/tokens",
                json=fake_token_data,
            )
            response = bucket_client.create_token(description="")
            assert response == fake_token_data

    def test_bucket__get_tokens(self, bucket_client, fake_token_data):
        data = [fake_token_data]
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v0/buckets/123/tokens", json=data
            )
            response = bucket_client.get_tokens()
            assert response == data

    def test_bucket__delete_token(self, bucket_client, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v0/buckets/123/tokens/8901",
                json=fake_token_data,
            )
            response = bucket_client.delete_token(token_uuid="8901")
            assert response == fake_token_data

    def test_bucket__push_data(self, bucket_client):
        rows = {"timestamp": "42", "data": []}
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v0/buckets/123/data", json=data)
            response = bucket_client.push_data(rows)
            assert response == data

    def test_bucket__get_data(self, bucket_client):
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v0/buckets/123/data", json=data)
            response = bucket_client.get_data()
            assert response == data


class TestAdacordApi:
    """Test the remaining helper functions in AdacordApi"""

    def test_http_client(self, fake_bucket_data):
        data = [fake_bucket_data]

        def callback(request, context):
            assert "Authorization" in request.headers
            return json.dumps(data)

        api = AdacordApi.Client(token="1234")
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v0/buckets", text=callback)
            api.Buckets.list()


class TestApiTokens:
    """Test API interface for Api Tokens"""

    def test_create_token(self, api, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v0/api_tokens",
                json=fake_token_data,
            )
            response = api.ApiTokens.create(description="")
            assert response == fake_token_data

    def test_get_tokens(self, api, fake_token_data):
        data = [fake_token_data]
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v0/api_tokens", json=data)
            response = api.ApiTokens.list()
            assert response == data

    def test_delete_token(self, api, fake_token_data):
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v0/api_tokens/8901",
                json=fake_token_data,
            )
            response = api.ApiTokens.delete(token_uuid="8901")
            assert response == fake_token_data


def test_bucket_args():
    bucket = BucketArgs(
        uuid="uuid",
        name="name",
        description="description",
        url="url",
        schemaless=True,
        enabled_google_pubsub_sa="my-gcp-sa",
        unexpected_field="unexpected_field",
    )
    assert bucket.uuid
    assert bucket.name
    assert bucket.description
    assert bucket.url
    assert bucket.schemaless
    assert bucket.enabled_google_pubsub_sa
