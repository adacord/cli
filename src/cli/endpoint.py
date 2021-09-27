import typer

from . import commons
from .api import AdacordApi

app = typer.Typer()


@app.command()
def create(name: str = typer.Option(...), schema: str = None):
    """
    Create a new endpoint with (optional) schema.
    """
    if schema:
        schema = commons.read_file(schema)
    payload = AdacordApi().add_endpoint(name, schema)
    typer.echo(
        f"Endpoint created, start sending data {payload['endpoint_url']}"
    )


@app.command()
def list():
    """
    Get a list of your endpoints.
    """
    payload = AdacordApi().list_endpoints()
    typer.echo(
        typer.style("Name \t\t\t URL", fg=typer.colors.WHITE, bold=True)
    )
    for row in payload:
        typer.echo(f" {row['name']} \t\t  {row['endpoint_url']}")


@app.command()
def query(name: str = typer.Option(...), query: str = typer.Option(...)):
    """
    Query your data using a SQL query
    """
    payload = AdacordApi().query_endpoint(name, query)
    for row in payload:
        typer.echo(row)
