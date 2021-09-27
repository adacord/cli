import typer

from .api import AdacordApi

app = typer.Typer()


@app.command()
def create(
    endpoint: str = typer.Option(...),
    query: str = typer.Option(...),
    url: str = typer.Option(...),
):
    """
    Add a webhook to your endpoints.
    """
    payload = AdacordApi().create_webhook(endpoint, query, url)
    typer.echo(f"Webhook created, start sending data {payload['url']}")
