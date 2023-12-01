"""
Advent of code: day XX
"""

import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    click.echo("todo")


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
