import typer

from . import commons
from .api import create_api
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
    password = typer.prompt(
        "> What's your password?", hide_input=True, confirmation_prompt=True
    )

    api = create_api()
    api.User.create(email, password)

    typer.echo(
        typer.style(
            "Awesome, check your email to confirm your email address!",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )


@app.command()
@cli_wrapper
def login(email: str = typer.Option(...)):
    """
    Login with the cli.
    """
    password = typer.prompt("> What's your password?", hide_input=True)
    api = create_api()
    response = api.User.login(email, password)
    auth = {"email": email, "token": response["access_token"]}
    commons.save_auth(auth)
