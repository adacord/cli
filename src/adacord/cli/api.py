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


class Client(requests.Session):
    def __init__(self, base_path: str, auth: AuthBase = None):
        super().__init__()
        self.auth: AuthBase = auth or AccessTokenAuth()
        self.base_path = base_path
        self.mount("http://", AdacordHTTPAdapter())
        self.mount("https://", AdacordHTTPAdapter())

    def request(self, method, url, *args, **kwargs):
        url = f"{self.base_path}{url}"
        response = super().request(
            method, url, timeout=HTTP_TIMEOUT, *args, **kwargs
        )
        if not response.ok:
            raise AdacordApiError(
                response.json(), status_code=response.status_code
            )
        return response


class User:
    def __init__(self, client: requests.Session):
        self.client = client

    def create(self, email: str, password: str):
        data = {"email": email, "password": password}
        self.client.post("/users", json=data, auth=False)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        response = self.client.post("/users/token", json=data, auth=False)
        return response.json()


class Bucket:
    def __init__(self, client: requests.Session):
        self.client = client

    def create(self, description: str, schemaless: bool):
        data = {"description": description, "schemaless": schemaless}
        response = self.client.post("/buckets", json=data)
        return response.json()

    def get(
        self, bucket: str = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if bucket:
            response = self.client.get(f"/buckets/{bucket}")
            return response.json()

        response = self.client.get("/buckets")
        return response.json()

    def delete(self, bucket: str) -> Dict[str, Any]:
        response = self.client.delete(f"/buckets/{bucket}")
        return response.json()

    def query(self, bucket: str, query: str):
        data = {"query": query}
        response = self.client.post(f"/buckets/{bucket}/query", json=data)
        return response.json()

    def create_webhook(
        self, bucket: str, query: str, url: str, description: str = None
    ):
        data = {"description": description, "query": query, "url": url}
        response = self.client.post(f"/buckets/{bucket}/webhooks", json=data)
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


class Adacrd:
    def client(self, bucket_name: str) -> requests.Session:
        client = Client(
            base_path=f"http://{bucket_name}.adacrd.in:8000/v1",
            auth=AccessTokenAuth(get_token),
        )
        return client

    def query(self, bucket_name: str, query: str):
        client = self.client(bucket_name)
        data = {"query": query}
        response = client.post("/query", json=data)
        return response.json()


class AdacordApi:
    def __init__(self, client=None):
        self.user = User(client)
        self.bucket = Bucket(client)
        self.adacrd = Adacrd()


def create_api() -> AdacordApi:
    client = Client(
        base_path="https://api.adacord.com/v1",
        auth=AccessTokenAuth(get_token),
    )
    return AdacordApi(client)


api = create_api()
