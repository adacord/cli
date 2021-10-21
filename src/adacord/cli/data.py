from pathlib import Path

import typer

from .api import create_api
from .commons import parse_csv
from .exceptions import cli_wrapper

app = typer.Typer()
token_app = typer.Typer(help="Manage API Tokens.")
app.add_typer(token_app, name="token")


@app.command("push")
@cli_wrapper
def push(
    filepath: Path = typer.Option(
        "The file path to the CSV file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    """
    Push the content of a CSV file to the bucket.
    """
    rows = parse_csv(filepath)

    api = create_api()
    api.Buckets.push(rows=rows)
    typer.echo(
        typer.style(
            "The data has been loaded 🚀.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
