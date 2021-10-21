from pathlib import Path

import pytest

from adacord.cli.commons import get_token, parse_csv, read_auth, save_auth


def test_write_read_auth(tmp_path):

    path = tmp_path / ".adacord"

    auth_payload = {"email": "my-email@email.com", "token": "my-token"}

    save_auth(auth_payload, path)

    assert read_auth(path) == auth_payload
    assert get_token(path) == auth_payload["token"]


@pytest.fixture
def csv_filepath(tmp_path: Path) -> Path:
    import csv

    filepath = tmp_path / "countries.csv"

    header = ["NAME", "area", "country_code2", "country_code3"]
    rows = [
        ["Albania", 28748, "AL", "ALB"],
        ["Algeria", 2381741, "DZ", "DZA"],
        ["American Samoa", 199, "AS", "ASM"],
        ["Andorra", 468, "AD", "AND"],
        ["Angola", 1246700, "AO", "AGO"],
    ]

    with filepath.open(mode="w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    yield filepath
    filepath.unlink()


def test_parse_csv(csv_filepath):
    rows = parse_csv(csv_filepath)
    assert rows
    assert rows == [
        {
            "area": "28748",
            "country_code2": "AL",
            "country_code3": "ALB",
            "name": "Albania",
        },
        {
            "area": "2381741",
            "country_code2": "DZ",
            "country_code3": "DZA",
            "name": "Algeria",
        },
        {
            "area": "199",
            "country_code2": "AS",
            "country_code3": "ASM",
            "name": "American Samoa",
        },
        {
            "area": "468",
            "country_code2": "AD",
            "country_code3": "AND",
            "name": "Andorra",
        },
        {
            "area": "1246700",
            "country_code2": "AO",
            "country_code3": "AGO",
            "name": "Angola",
        },
    ]
