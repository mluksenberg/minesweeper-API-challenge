import datetime

import click
from pip._vendor import requests


def _draw_cell(cell):
    if cell.get("status") == "DISCOVERED":
        return show_value(cell)
    elif cell.get("status") == "UNKNOWN":
        return " * "
    elif cell.get("status") == "QUESTION":
        return " ? "
    elif cell.get("status") == "FLAG":
        return " P "
    else:
        if cell.get("has_mine"):
            return " M "
        else:
            return " _ "


def show_value(cell):
    if cell.get("has_mine"):
        return " M "
    else:
        return f" {cell.get('value')} "


def _draw_current_board(response):
    cells = response.get("board")
    rows_size = max(
        map(lambda x: x.get("coordinate_y"), response.get("board"))) + 1
    for i in range(rows_size):
        row = list(filter(lambda x: x.get("coordinate_y") == i, cells))
        click.echo("".join(map(lambda r: _draw_cell(r), row)))


def _discover_board(response):
    cells = response.get("board")
    rows_size = max(
        map(lambda x: x.get("coordinate_y"), response.get("board"))) + 1
    for i in range(rows_size):
        row = list(filter(lambda x: x.get("coordinate_y") == i, cells))
        click.echo("".join(map(lambda r: show_value(r), row)))


def _get_game_url(env, game_id=None):
    endpoint = "https://mluksenberg-minesweeper.herokuapp.com" \
        if env == "dev" else "http://localhost:5000"
    return f"{endpoint}/api/game{'/' + game_id if game_id else ''}"


def _set_cell_action(ctx, game_id, coordinates, action):
    url = _get_game_url(ctx.obj["ENV"], game_id)
    response = requests.put(url, json={"coordinate_x": coordinates[0],
                                       "coordinate_y": coordinates[1],
                                       "action": action}
                            )
    if response.status_code != 200:
        click.echo(click.style(f"Error: {response.json()}", fg="red"))
    elif ctx.obj["DEBUG"]:
        rows_size = max(
            map(lambda x: x.get("coordinate_x"),
                response.json().get("board"))) + 1
        _draw_game_context(response.json())
        click.echo("=" * rows_size * 3)
        _draw_current_board(response.json())


@click.group()
@click.option("--debug",
              "-d",
              default=False,
              is_flag=True,
              help="Set it as true if you want to see the board")
@click.option("--env",
              "-e",
              default="local",
              required=False,
              type=str,
              help="Specify the environment dev or local")
@click.pass_context
def cli(ctx, debug, env):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    ctx.obj["ENV"] = env


@cli.command()
@click.argument("game_id", required=True, nargs=1)
@click.pass_context
def show_board(ctx, game_id):
    url = _get_game_url(ctx.obj["ENV"], game_id)
    response = requests.get(url).json()
    rows_size = max(
        map(lambda x: x.get("coordinate_x"), response.get("board"))) + 1
    _draw_game_context(response)
    click.echo("=" * rows_size * 3)
    _draw_current_board(response)
    if ctx.obj["DEBUG"]:
        click.echo("=" * rows_size * 3)
        _discover_board(response)


def _draw_game_context(response):
    time = datetime.datetime.utcfromtimestamp(
        datetime.datetime.utcnow().timestamp() - response.get(
            "datetime")).strftime("%H:%m:%S")
    status = response.get("status")
    click.echo(f"Status: {status}\nClock: {time}")


@cli.command()
@click.argument("game_id",
                required=True,
                nargs=1)
@click.argument("coordinates",
                required=True,
                nargs=2)
@click.pass_context
def discover_cell(ctx, game_id, coordinates):
    _set_cell_action(ctx, game_id, coordinates, "DISCOVER")


@cli.command()
@click.argument("game_id",
                required=True,
                nargs=1)
@click.argument("coordinates",
                required=True,
                nargs=2)
@click.pass_context
def set_flag(ctx, game_id, coordinates):
    _set_cell_action(ctx, game_id, coordinates, "MARK_FLAG")


@cli.command()
@click.argument("game_id",
                required=True,
                nargs=1)
@click.argument("coordinates",
                required=True,
                nargs=2)
@click.pass_context
def set_question(ctx, game_id, coordinates):
    _set_cell_action(ctx, game_id, coordinates, "MARK_QUESTION")


@cli.command()
@click.argument("game_id",
                required=True,
                nargs=1)
@click.argument("coordinates",
                required=True,
                nargs=2)
@click.pass_context
def set_unknown(ctx, game_id, coordinates):
    _set_cell_action(ctx, game_id, coordinates, "MARK_UNKNOWN")


@cli.command()
@click.argument("mines",
                required=True,
                nargs=1)
@click.argument("width",
                required=True,
                nargs=1)
@click.argument("height",
                required=True,
                nargs=1)
@click.pass_context
def create_game(ctx, mines, width, height):
    url = _get_game_url(ctx.obj["ENV"])
    response = requests.post(url,
                             json={"mines": mines,
                                   "width": width,
                                   "height": height})
    if response.status_code != 200:
        click.echo(click.style(f"Error: {response.json()}", fg="red"))
    else:
        click.echo(f"Game Created with ID: {response.json().get('id')}")


if __name__ == '__main__':
    cli(obj={})
