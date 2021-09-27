from typing import Any, Dict


class AdacordApi:
    def __init__(self, client=None):
        self.client = client

    def create_user(self, email: str, password: str):
        pass

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
