import typer

from . import user, bucket

app = typer.Typer()
app.add_typer(user.app, name="user")
app.add_typer(bucket.app, name="bucket")
