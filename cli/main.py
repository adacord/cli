import typer

from . import bucket, user, webhook

app = typer.Typer()
app.add_typer(user.app, name="user")
app.add_typer(bucket.app, name="bucket")
app.add_typer(webhook.app, name="webhook")
