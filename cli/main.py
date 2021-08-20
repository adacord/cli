import typer

from . import endpoint, user, webhook

app = typer.Typer()
app.add_typer(user.app, name="user")
app.add_typer(endpoint.app, name="endpoint")
app.add_typer(webhook.app, name="webhook")
