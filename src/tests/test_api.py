class TestUser:
    def test_user__create(self, requests_mock, api):
        data = {
            "uid": "user_record.uid",
            "display_name": "user_record.uid",
            "email": "user_record.uid",
            "phone_number": "user_record.uid",
            "photo_url": "user_record.uid",
            "email_verified": "user_record.uid",
        }

        requests_mock.post("http://fake.example:8000/v1/users", json=data)
        api.user.create("email", "password")

    def test_user__login(self, requests_mock, api):
        data = {
            "access_token": "",
            "refresh_token": "",
            "user_email": "",
            "expires_in": "",
        }
        requests_mock.post(
            "http://fake.example:8000/v1/users/token", json=data
        )
        response = api.user.login("email", "password")
        assert response


class TestBucket:
    def test_bucket__create(self, requests_mock, api):
        data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.post("http://fake.example:8000/v1/buckets", json=data)
        response = api.bucket.create("my-bucket")
        assert response == data

    def test_bucket__get_all(self, requests_mock, api):
        data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.get("http://fake.example:8000/v1/buckets", json=data)
        response = api.bucket.get()
        assert response

    def test_bucket_get_single(self, requests_mock, api):
        data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.get(
            "http://fake.example:8000/v1/buckets/my-bucket", json=data
        )
        response = api.bucket.get("my-bucket")
        assert response

    def test_bucket__delete(self, requests_mock, api):
        data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.delete(
            "http://fake.example:8000/v1/buckets/email", json=data
        )
        response = api.bucket.delete("email")
        assert response

    def test_bucket__webhook_create(self, requests_mock, api):
        data = {"uuid": "", "name": {}, "url": "https://your-bucket.ada.in"}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.post(
            "http://fake.example:8000/v1/buckets/my-bucket/webhooks", json=data
        )
        response = api.bucket.create_webhook(
            "my-bucket",
            "select * from my-bucket",
            "https://my-webhook-url.com",
        )
        assert response


class TestAdacrd:
    def test_adacrd__query(self, requests_mock, api):
        data = {"query": "", "result": []}
        # data = {
        #     "description": "",
        #     "data_schema": {},
        # }
        requests_mock.post(
            "http://fake.example:8000/v1/buckets/email/query", json=data
        )
        response = api.bucket.query("email", "select * from my-bucket")
        assert response
