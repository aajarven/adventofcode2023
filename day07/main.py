"""
Advent of code: day 07
"""

import click

from hand import Hand1, Hand2


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    input_lines = input_file.readlines()

    hands = [Hand1(input_line) for input_line in input_lines]
    click.echo(f"part 1: {total_winnings(hands)}")

    hands = [Hand2(input_line) for input_line in input_lines]
    click.echo(f"part 2: {total_winnings(hands)}")


def total_winnings(hands):
    """
    Calculate the total winnings for given hands.
    """
    hands.sort()
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
    return total


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
