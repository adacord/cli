import json
from pathlib import Path

CONFIG_FOLDER_PATH = Path.home() / ".adacord"


def save_token(payload):
    Path(CONFIG_FOLDER_PATH).mkdir(exist_ok=True)
    with open(CONFIG_FOLDER_PATH / "auth.json", "w+") as f:
        f.write(json.dumps(payload))


def read_token(token):
    with open(CONFIG_FOLDER_PATH / "auth.json", "r+") as f:
        return json.loads(f.read())


def read_file(path: str):
    with open(path, "r+") as f:
        return f.read()
