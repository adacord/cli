import typer

from . import commons
from .api import api
from .exceptions import cli_wrapper

app = typer.Typer()


@app.command()
@cli_wrapper
def create():
    """
    Create a new user.
    """
    typer.echo("Hey there 👋")

    email = typer.prompt("> What's your email?")
    password = typer.prompt("> What's your password?", hide_input=True)
    api.user.create(email, password)

    typer.echo(
        typer.style(
            "Awesome, check your email to confirm your email address",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )


@app.command()
@cli_wrapper
def login(email: str = typer.Option(...), password: str = typer.Option(...)):
    """
    Login with the cli.
    """
    response = api.user.login(email, password)
    auth = {"email": email, "token": response["access_token"]}
    commons.save_auth(auth)
