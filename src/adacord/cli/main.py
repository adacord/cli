import typer

from . import data, user, bucket

app = typer.Typer()
app.add_typer(user.app, name="user")
app.add_typer(bucket.app, name="bucket")
app.add_typer(data.app, name="data")
