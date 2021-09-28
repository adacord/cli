import json
from pathlib import Path

CONFIG_FOLDER_PATH = Path.home() / ".adacord"


def save_auth(payload, base_path=CONFIG_FOLDER_PATH):
    Path(base_path).mkdir(exist_ok=True)
    with open(base_path / "auth.json", "w+") as f:
        f.write(json.dumps(payload))


def read_auth(base_path=CONFIG_FOLDER_PATH):
    with open(base_path / "auth.json", "r+") as f:
        return json.loads(f.read())


def get_token(base_path=CONFIG_FOLDER_PATH):
    auth = read_auth(base_path)
    return auth["token"]
