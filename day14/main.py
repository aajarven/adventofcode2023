"""
Advent of code: day 14
"""

import click

from rocks import Rocks


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    symbols = read_symbols(input_file)
    rocks = Rocks(symbols)
    rocks.slide_up()
    click.echo(f"Part 1: {rocks.load}")

    rocks = Rocks(symbols)
    history = []
    total_cycles = 1000000000
    for i in range(total_cycles):
        if rocks in history:
            cycle_start = history.index(rocks)
            cycle_length = i - cycle_start
            last_setup_index = (total_cycles - cycle_start) % cycle_length + cycle_start
            last_rocks = history[last_setup_index]
            break
        history.append(rocks)
        rocks = rocks.cycled

    click.echo(f"part 2: {last_rocks.load}")


def read_symbols(input_file):
    """
    Read the rocks from input file into a 2D array.

    The rocks are represented as '#' (stationary rocks) or 'O' (rolling rocks).
    Empty spaces '.'.
    """
    rocks = []
    for line in input_file.readlines():
        new_line = []
        for char in line.strip():
            new_line.append(char)
        rocks.append(new_line)
    return rocks


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
