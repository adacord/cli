from typing import Any, Dict
import requests


class Client:
    def __init__(self, client=None, base_path="https://api.adacord.com"):
        self.client = client
        if client is None:
            self.client = requests

        self.base_path = base_path

    def post(self, path, json):
        full_path = f"{self.base_path}/{path}"
        return self.client.post(full_path, json=json)


class AdacordApi:
    def __init__(self, client=None):
        self.client = client

    def create_user(self, email: str, password: str):
        data = {"email": email, "password": password}
        r = self.client.post("/users", json=data)
        print(r.content)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        return {"token": "your-token"}

    def add_endpoint(self, name: str, schema: str):
        return {"endpoint_url": f"https//dcrd.com/djHS/{name}"}

    def create_webhook(self, name: str, query: str, url: str):
        return {"id": "random-id", "endpoint": name, "url": url}

    def list_endpoints(self):
        return [
            {
                "name": "my-endpoint-1",
                "endpoint_url": "https//dcrd.com/djHS/my-endpoint-1",
            },
            {
                "name": "my-endpoint-2",
                "endpoint_url": "https//dcrd.com/djHS/my-endpoint-2",
            },
        ]

    def query_endpoint(self, name: str, query: str):
        return [
            {
                "name": "random-name",
                "field_1": "my-field",
            },
            {
                "name": "random-name",
                "field_2": "my-field",
            },
        ]


api = AdacordApi(Client())
