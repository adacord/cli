from typing import Any, Dict, List, Union

import requests

from .commons import get_token
from .exceptions import AdacordApiError


class Client:
    def __init__(
        self, client=None, base_path="https://api.adacord.com", get_token=None
    ):
        self.client = client
        if client is None:
            self.client = requests

        self.get_token = get_token
        self.base_path = base_path

    def auth(self):
        return {"authorization": f"Bearer {self.get_token()}"}

    def post(self, path, json, auth=True):
        full_path = f"{self.base_path}{path}"

        headers = {}
        if auth:
            headers = self.auth()

        r = self.client.post(full_path, json=json, headers=headers)

        if (r.status_code // 100) > 2:
            raise AdacordApiError(r.json(), status_code=r.status_code)

        return r.json()

    def get(self, path, params=None, auth=True):
        full_path = f"{self.base_path}{path}"

        headers = {}
        if auth:
            headers = self.auth()

        r = self.client.get(full_path, params=params, headers=headers)

        if (r.status_code // 100) > 2:
            raise AdacordApiError(r.json(), status_code=r.status_code)

        return r.json()

    def delete(self, path, auth=True):
        full_path = f"{self.base_path}{path}"

        headers = {}
        if auth:
            headers = self.auth()

        r = self.client.delete(full_path, headers=headers)

        if (r.status_code // 100) > 2:
            raise AdacordApiError(r.json(), status_code=r.status_code)

        return r.json()


class User:
    def __init__(self, instance):
        self.client = instance.client

    def create(self, email: str, password: str):
        data = {"email": email, "password": password}
        self.client.post("/users", json=data, auth=False)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        return self.client.post("/token", json=data, auth=False)


class Bucket:
    def __init__(self, instance):
        self.client = instance.client

    def create(self, description: str):
        data = {"description": description}
        return self.client.post("/buckets", json=data)

    def get(
        self, bucket: str = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if bucket:
            return self.client.get(f"/buckets/{bucket}")

        return self.client.get("/buckets")

    def delete(self, bucket: str) -> Dict[str, Any]:
        return self.client.delete(f"/buckets/{bucket}")

    def query(self, bucket: str, query: str):
        data = {"query": query}
        return self.client.post(f"/buckets/{bucket}/query", json=data)

    def create_webhook(
        self, bucket: str, query: str, url: str, description: str = None
    ):
        data = {"description": description, "query": query, "url": url}
        return self.client.post(f"/buckets/{bucket}/webhooks", json=data)


class AdacordApi:
    def __init__(self, client=None):
        self.client = client

        self.user = User(self)
        self.bucket = Bucket(self)


api = AdacordApi(Client(get_token=get_token))
