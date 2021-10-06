from adacord.cli.commons import get_token, read_auth, save_auth


def test_write_read_auth(tmp_path):

    path = tmp_path / ".adacord"

    auth_payload = {"email": "my-email@email.com", "token": "my-token"}

    save_auth(auth_payload, path)

    assert read_auth(path) == auth_payload
    assert get_token(path) == auth_payload["token"]
