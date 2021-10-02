import typer
from tabulate import tabulate

from .api import api
from .exceptions import cli_wrapper

app = typer.Typer()
token_app = typer.Typer(help="Manage API Tokens.")
app.add_typer(token_app, name="token")


@app.command("create")
@cli_wrapper
def create_bucket(description: str = typer.Option("")):
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
    first_row = ("ID", "Description", "URL")
    typer.echo(
        tabulate(
            [first_row, values], headers="firstrow", tablefmt="fancy_grid"
        )
    )


@app.command("list")
@cli_wrapper
def list_bucket():
    """
    Get a list of your buckets.
    """
    payload = api.bucket.get()
    first_row = ("uuid", "description", "url")

    if not payload:
        typer.echo(
            typer.style(
                "Ohhhh... no buckets :)", fg=typer.colors.MAGENTA, bold=True
            )
        )
        return

    rows = []
    for index, row in enumerate(payload, 1):
        rows.append([index, *[row[entry] for entry in first_row]])

    first_row = ("ID", "Description", "URL")
    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@app.command("delete")
@cli_wrapper
def delete_bucket(bucket: str):
    """
    Delete a bucket.
    """
    api.bucket.delete(bucket)
    typer.echo(
        typer.style(
            f"Bucket {bucket} deleted.", fg=typer.colors.WHITE, bold=True
        )
    )


@app.command("query")
@cli_wrapper
def query_bucket(
    bucket: str = typer.Option(...), query: str = typer.Option(...)
):
    """
    Query a bucket using a SQL query.
    """
    payload = api.bucket.query(bucket, query)
    for row in payload:
        typer.echo(row)


@token_app.command("create")
@cli_wrapper
def create_token(
    bucket: str = typer.Argument(
        ..., help="The bucket uuid you want to give access to."
    ),
    description: str = typer.Option(""),
):
    """
    Create a new API Token.
    """
    payload = api.bucket.create_token(bucket, description)
    typer.echo(
        typer.style(
            "API Token created.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    typer.echo(
        typer.style(
            "⚠️  PLEASE SAVE THE TOKEN, THIS IS THE ONLY TIME WHERE WE DISPLAY IT ⚠️",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    first_row = ("uuid", "token", "description", "created_on")
    values = [payload[entry] for entry in first_row]
    first_row = ("ID", "Token", "Description", "Created on")
    typer.echo(
        tabulate(
            [first_row, values], headers="firstrow", tablefmt="fancy_grid"
        )
    )


@token_app.command("list")
@cli_wrapper
def list_tokens(
    bucket: str = typer.Argument(
        ..., help="The bucket uuid you want to give access to."
    )
):
    """
    Get your tokens.
    """
    tokens = api.bucket.get_tokens(bucket)
    first_row = ("uuid", "token", "description", "created_on")
    if not tokens:
        typer.echo(
            typer.style(
                f"No tokens for Bucket({bucket}).",
                fg=typer.colors.WHITE,
                bold=True,
            )
        )
        return

    rows = []
    for index, row in enumerate(tokens, 1):
        rows.append([index, *[row[entry] for entry in first_row]])

    first_row = ("ID", "Token", "Description", "Created on")
    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@token_app.command("delete")
@cli_wrapper
def delete_token(bucket: str, token: str):
    """
    Delete an API Token.
    """
    api.bucket.delete_token(bucket, token)
    typer.echo(
        typer.style(
            f"API Token {token} deleted.", fg=typer.colors.WHITE, bold=True
        )
    )
