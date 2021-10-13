import pytest
import requests
import requests_mock
from requests import Request
from requests.auth import AuthBase

from adacord.cli.api import (
    Bucket,
    ApiClient,
    AdacordApi,
    HTTPClient,
    AdacrdClient,
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
        api_client = AdacrdClient(bucket_name="dump", client=http_client)
        assert api_client
        assert api_client.client == http_client
        assert api_client.bucket_name == "dump"

    def test_base_path(self, http_client):
        api_client = AdacrdClient(bucket_name="dump", client=http_client)
        assert api_client.base_path == "https://dump.adacrd.in"

    def test_url_for(self, http_client):
        api_client = AdacrdClient(bucket_name="dump", client=http_client)
        result = api_client.url_for("/test")
        assert result == "https://dump.adacrd.in/v1/test"


class TestUser:
    """Test the endpoints that deal with users"""

    def test_create(self, api):
        client = api.User
        data = {
            "uid": "123456",
            "display_name": "fake user",
            "email": "fake@adacord.com",
            "phone_number": "+123456",
            "photo_url": "https+fake://test.photo.here",
            "email_verified": "false",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v1/users", json=data)
            client.create("email", "password")

    def test_login(self, api):
        client = api.User
        data = {
            "access_token": "",
            "refresh_token": "",
            "user_email": "",
            "expires_in": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v1/users/token", json=data)
            response = client.login("email", "password")
            assert response


class TestBuckets:
    """Test the endpoints that deal with buckets"""

    def test_create(self, api):
        client = api.Buckets
        data = {
            "uuid": "123",
            "name": {},
            "url": "https://your-bucket.ada.in",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v1/buckets", json=data)
            response = client.create("123", schemaless=False)
            assert response
            assert response == data

    def test_get_all(self, api):
        client = api.Buckets
        data = [
            {
                "uuid": "123",
                "name": {},
                "url": "https://your-bucket.ada.in",
                "description": "",
            }
        ]
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v1/buckets/", json=data)
            response = client.get()
            assert response
            assert response[0].uuid == data[0]["uuid"]
            assert response[0].name == data[0]["name"]
            assert response[0].url == data[0]["url"]
            assert response[0].description == data[0]["description"]

    def test_get_single(self, api):
        client = api.Buckets
        data = {
            "uuid": "123",
            "name": {},
            "url": "https://your-bucket.ada.in",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v1/buckets/123", json=data)
            response = client.get("123")
            assert response

    def test_delete(self, api):
        client = api.Buckets
        data = {
            "uuid": "123",
            "name": {},
            "url": "https://your-bucket.ada.in",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.delete("https://api.adacord.com/v1/buckets/123", json=data)
            response = client.delete("123")
            assert response


class TestAPITokens:
    """Test the endpoints that deal with user-managed tokens"""

    def test_create_token(self, api):
        client = api.Buckets
        data = {
            "uuid": "8901",
            "created_on": {},
            "token": "tEsTtOkEn",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v1/buckets/123/tokens", json=data
            )
            response = client.create_token(bucket="123", description="")
            assert response
            assert response == data

    def test_get_tokens(self, api):
        client = api.Buckets
        data = [
            {
                "uuid": "8901",
                "created_on": {},
                "token": "tEsTtOkEn",
                "description": "",
            }
        ]
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v1/buckets/123/tokens", json=data
            )
            response = client.get_tokens(bucket="123")
            assert response
            assert response == data

    def test_delete_token(self, api):
        client = api.Buckets
        data = [
            {
                "uuid": "8901",
                "created_on": {},
                "token": "tEsTtOkEn",
                "description": "",
            }
        ]
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v1/buckets/123/tokens/8901", json=data
            )
            response = client.delete_token(bucket="123", token_uuid="8901")
            assert response
            assert response == data


@pytest.fixture
def bucket_client(api) -> Bucket:
    bucket = {
        "uuid": "123",
        "name": "buckety",
        "url": "https://your-bucket.ada.in",
        "description": "",
    }
    with requests_mock.Mocker() as mock:
        mock.get("https://api.adacord.com/v1/buckets/123", json=bucket)
        client = api.Bucket("123")
        yield client


class TestBucket:
    """Test the endpoints that deal with bucket data"""

    def test_get(self, api):
        data = {
            "uuid": "123",
            "name": "buckety",
            "url": "https://your-bucket.ada.in",
            "description": "test",
        }
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v1/buckets/123", json=data)
            response = api.Bucket("123")
            assert response
            assert response.uuid
            assert response.name
            assert response.description
            assert response.url

    def test_delete(self, bucket_client):
        data = {"uuid": "123"}
        with requests_mock.Mocker() as mock:
            mock.delete("https://api.adacord.com/v1/buckets/123", json=data)
            response = bucket_client.delete()
            assert response == data

    def test_create_token(self, bucket_client):
        data = {
            "uuid": "8901",
            "created_on": {},
            "token": "tEsTtOkEn",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://api.adacord.com/v1/buckets/123/tokens", json=data
            )
            response = bucket_client.create_token(description="")
            assert response == data

    def test_get_tokens(self, bucket_client):
        data = [
            {
                "uuid": "8901",
                "created_on": {},
                "token": "tEsTtOkEn",
                "description": "",
            }
        ]
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://api.adacord.com/v1/buckets/123/tokens", json=data
            )
            response = bucket_client.get_tokens()
            assert response == data

    def test_delete_token(self, bucket_client):
        data = [
            {
                "uuid": "8901",
                "created_on": {},
                "token": "tEsTtOkEn",
                "description": "",
            }
        ]
        with requests_mock.Mocker() as mock:
            mock.delete(
                "https://api.adacord.com/v1/buckets/123/tokens/8901", json=data
            )
            response = bucket_client.delete_token(token_uuid="8901")
            assert response == data

    def test_query(self, bucket_client):
        data = {"query": "", "result": []}
        with requests_mock.Mocker() as mock:
            mock.post("https://buckety.adacrd.in/v1/query", json=data)
            response = bucket_client.query("select * from my-bucket")
            assert response == data

    def test_push(self, bucket_client):
        rows = {"timestamp": "42", "data": []}
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.post("https://buckety.adacrd.in/v1/", json=data)
            response = bucket_client.push(rows)
            assert response == data

    def test_fetch_all(self, bucket_client):
        data = {"result": []}
        with requests_mock.Mocker() as mock:
            mock.get("https://buckety.adacrd.in/v1/", json=data)
            response = bucket_client.fetch_all()
            assert response == data


class TestAdacordApi:
    """Test the remaining helper functions in AdacordApi"""

    def test_client(self):
        api = AdacordApi.Client(token="1234")
        assert api
        assert api.client

    def test_create_bucket(self, api):
        data = {
            "uuid": "123",
            "name": {},
            "url": "https://your-bucket.ada.in",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://api.adacord.com/v1/buckets", json=data)
            response = api.create_bucket(description="", schemaless=False)
            assert response
            assert response == data

    def test_get_bucket(self, api):
        data = {
            "uuid": "123",
            "name": {},
            "url": "https://your-bucket.ada.in",
            "description": "",
        }
        with requests_mock.Mocker() as mock:
            mock.get("https://api.adacord.com/v1/buckets/123", json=data)
            response = api.get_bucket(bucket_uuid="123")
            assert response
            assert response.uuid == data["uuid"]
            assert response.name == data["name"]
            assert response.description == data["description"]
            assert response.url == data["url"]
