import typer
from tabulate import tabulate

from .api import api
from .exceptions import cli_wrapper

app = typer.Typer()


@app.command()
def create(description: str = typer.Option(...)):
    """
    Create a new bucket.
    """
    payload = api.bucket.create(description)
    typer.echo(
        typer.style(
            "Bucket created, you can start sending data 🚀",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    first_row = ("uuid", "name", "description", "url")
    values = [payload[entry] for entry in first_row]
    typer.echo(
        tabulate(
            [first_row, values], headers="firstrow", tablefmt="fancy_grid"
        )
    )


@app.command()
@cli_wrapper
def list():
    """
    Get a list of your buckets.
    """
    payload = api.bucket.get()
    first_row = ("uuid", "name", "description", "url")

    rows = []
    for index, row in enumerate(payload, 1):
        rows.append([index, *[row[entry] for entry in first_row]])

    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@app.command()
def delete(bucket: str):
    """
    Delete a bucket.
    """
    payload = api.bucket.delete(bucket)
    print(payload)
    typer.echo(
        typer.style(
            f"Bucket {bucket} deleted.", fg=typer.colors.WHITE, bold=True
        )
    )


@app.command()
def query(bucket: str = typer.Option(...), query: str = typer.Option(...)):
    """
    Query a bucket using a SQL query
    """
    payload = api.bucket.query(bucket, query)
    for row in payload:
        typer.echo(row)
