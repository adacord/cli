import typer

from . import commons
from .api import api

app = typer.Typer()


@app.command()
def create():
    """
    Create a new user.
    """
    typer.echo("Hey there 👋")

    email = typer.prompt("> What's your email?")
    password = typer.prompt("> What's your password?", hide_input=True)
    api.create_user(email, password)

    typer.echo("Awesome, check your email!")


@app.command()
def login(email: str = typer.Option(...), password: str = typer.Option(...)):
    """
    Login with the cli.
    """
    payload = AdacordApi().login(email, password)
    auth = {"email": email, "token": payload["token"]}
    commons.save_token(auth)
