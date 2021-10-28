import typer

from . import auth, bucket

app = typer.Typer()
app.add_typer(auth.user, name="user")
app.command("login")(auth.login_with_email_or_token)
app.command("logout")(auth.logout)
app.add_typer(bucket.app, name="bucket")
