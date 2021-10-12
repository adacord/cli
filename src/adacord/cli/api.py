import urllib
from dataclasses import dataclass
from functools import partialmethod
from typing import Any, Dict, List, Union, Callable

import requests
from requests.auth import AuthBase

from .commons import get_token
from .exceptions import AdacordApiError

HTTP_TIMEOUT = 10


class AccessTokenAuth(AuthBase):
    def __init__(self, token_getter: Callable[[], str]):
        self._token_getter = token_getter
        self._token = None

    def get_token(self):
        if not self._token:
            self._token = self._token_getter()
        return self._token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.get_token()}"
        return request


class AdacordHTTPAdapter(requests.adapters.HTTPAdapter):
    """
    This Adapter is responsible for retrying the failed requests (with exponential backoff)
    """

    def send(self, req, *args, **kwargs):
        response = super().send(req, *args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise AdacordApiError(
                response.json(), status_code=response.status_code
            ) from error
        else:
            return response


class HTTPClient(requests.Session):
    def __init__(self, auth: AuthBase = None):
        super().__init__()
        self.auth: AuthBase = auth or AccessTokenAuth()
        self.mount("http://", AdacordHTTPAdapter())
        self.mount("https://", AdacordHTTPAdapter())

    def request(self, method, url, *args, **kwargs):
        response = super().request(
            method, url, timeout=HTTP_TIMEOUT, *args, **kwargs
        )
        if not response.ok:
            raise AdacordApiError(
                response.json(), status_code=response.status_code
            )
        return response

    @classmethod
    def with_token(cls, token: str) -> "HTTPClient":
        return HTTPClient(auth=AccessTokenAuth(token))


class ApiClient:
    """Client for the Adacord API"""

    def __init__(self, client: HTTPClient):
        self.client = client

    @property
    def base_path(self) -> str:
        return "https://api.adacord.com/v1"

    def url_for(self, endpoint: str) -> str:
        return urllib.parse.urljoin(self.base_path, endpoint)


class AdacrdClient(ApiClient):
    """Client for the Adacrd Bucket API"""

    def __init__(self, bucket_name: str, client: HTTPClient):
        super().__init__(client)
        self.bucket_name = bucket_name

    @property
    def base_path(self) -> str:
        return f"https://{self.bucket_name}.adacrd.in/v1"


class User(ApiClient):
    def create(self, email: str, password: str):
        data = {"email": email, "password": password}
        self.client.post(self.url_for("/users"), json=data, auth=False)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        response = self.client.post(
            self.url_for("/users/token"), json=data, auth=False
        )
        return response.json()


class Bucket:
    def __init__(self, client: requests.Session):
        self.client = client

    def create(self, description: str, schemaless: bool):
        data = {"description": description, "schemaless": schemaless}
        response = self.client.post("/buckets", json=data)
        return response.json()

    def _bucket_from_payload(self, bucket_payload: Dict[str, Any]) -> "Bucket":
        return Bucket(bucket_name=bucket_payload["name"], client=self.client)

    # TODO: get by name as well
    def get(self, bucket: str = None) -> Union["Bucket", List["Bucket"]]:
        if bucket:
            endpoint = f"/buckets/{bucket}"
        else:
            endpoint = "/buckets/"

        url = self.url_for(endpoint)
        response = self.client.get(url)
        bucket_payload = response.json()
        if not isinstance(bucket_payload, list):
            bucket_payload = [bucket_payload]

        return [
            self._bucket_from_payload(payload) for payload in bucket_payload
        ]

    def delete(self, bucket: str) -> Dict[str, Any]:
        response = self.client.delete(f"/buckets/{bucket}")
        return response.json()

    def create_token(self, bucket: str, description: str = None):
        data = {"description": description}
        response = self.client.post(f"/buckets/{bucket}/tokens", json=data)
        return response.json()

    def get_tokens(self, bucket: str):
        response = self.client.get(f"/buckets/{bucket}/tokens")
        return response.json()

    def delete_token(self, bucket: str, token_uuid: str):
        response = self.client.delete(f"/buckets/{bucket}/tokens/{token_uuid}")
        return response.json()


@dataclass
class BucketArgs:
    uuid: str
    name: str
    description: str
    url: str


class Bucket(AdacrdClient):
    def __init__(
        self,
        bucket_payload: BucketArgs,
        client: HTTPClient,
        buckets_router: "Buckets",
    ):
        super().__init__(bucket_payload.name, client=client)
        self.uuid = bucket_payload.uuid
        self.name = bucket_payload.name
        self.description = bucket_payload.description
        self.url = bucket_payload.url
        self._buckets_router = buckets_router

    def delete(self) -> Dict[str, Any]:
        return self._buckets_router.delete(self.bucket_name)

    def create_token(self, description: str = None) -> Dict[str, Any]:
        return self._buckets_router.create_token(self.bucket_name, description)

    def get_tokens(self) -> List[Dict[str, Any]]:
        return self._buckets_router.get_tokens(self.bucket_name)

    def delete_token(self, token_uuid: str) -> Dict[str, Any]:
        return self._buckets_router.delete_token(self.bucket_name, token_uuid)

    def query(self, query: str) -> List[Dict[str, Any]]:
        data = {"query": query}
        response = self.client.post(self.url_for("/query"), json=data)
        return response.json()

    def insert_rows(self, rows: List[Dict[str, Any]]):
        data = {"data": rows}
        response = self.client.post(self.url_for("/"), json=data)
        return response.json()

    def fetch_all(self) -> List[Dict[str, Any]]:
        response = self.client.get(self.url_for("/"))
        return response.json()


class AdacordApi:
    def __init__(self, client: HTTPClient = None):
        self.client = client or HTTPClient(auth=AccessTokenAuth(get_token))

    @property
    def User(self) -> User:
        return User(self.client)

    @property
    def Buckets(self) -> Buckets:
        return Buckets(self.client)

    def Bucket(self, bucket_name: str) -> Bucket:
        bucket_payload = self.Buckets.get(bucket_name)
        return Bucket(
            bucket_payload,
            client=self.client,
            buckets_router=self.Buckets,
        )

    @classmethod
    def Client(cls, token: str) -> "AdacordApi":
        client = HTTPClient.with_token(token)
        return cls(client)

    def create_bucket(self, description: str) -> Bucket:
        return self.Buckets.create(description)

    def get_bucket(self, bucket_name: str) -> Bucket:
        return self.Buckets.get(bucket_name)


def create_api() -> AdacordApi:
    return AdacordApi()
