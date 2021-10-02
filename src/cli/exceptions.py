import functools
from json import JSONDecodeError

import typer


class AdacordApiError(Exception):
    def __init__(self, message, status_code):
        if isinstance(message, dict):
            if "message" in message:
                self.message = message["message"]
        else:
            self.message = message

        self.status_code = status_code


def cli_wrapper(func):
    """Catch execpetions and return cli printable errors."""

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AdacordApiError as err:
            typer.echo(
                typer.style(
                    f"Error: {err.message}", fg=typer.colors.RED, bold=True
                )
            )
        except JSONDecodeError:
            typer.echo(
                typer.style(
                    "Ouch.... something bad happed :/",
                    fg=typer.colors.RED,
                    bold=True,
                )
            )

    return decorator
