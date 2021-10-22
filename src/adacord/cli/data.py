from enum import Enum
from pathlib import Path

import typer

from .api import create_api
from .commons import parse_csv, parse_json, parse_jsonlines
from .exceptions import cli_wrapper

app = typer.Typer()


class DataFileFormat(str, Enum):
    csv = "csv"
    json = "json"
    jsonlines = "jsonlines"


@app.command("push")
@cli_wrapper
def push(
    filepath: Path = typer.Option(
        "The path to the data file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    format: DataFileFormat = typer.Option(
        "The format of the data file", case_sensitive=False
    ),
):
    """
    Push the content of a CSV file to the bucket.
    """
    if format == DataFileFormat.csv:
        rows = parse_csv(filepath)
    elif format == DataFileFormat.json:
        rows = parse_json(filepath)
    elif format == DataFileFormat.csv:
        rows = parse_jsonlines(filepath)

    api = create_api()
    api.Buckets.push(rows=rows)
    typer.echo(
        typer.style(
            "The data has been loaded 🚀.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
