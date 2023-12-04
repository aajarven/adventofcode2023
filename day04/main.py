"""
Advent of code: day 04
"""

import click

from card import Card


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    cards = [Card(line) for line in input_file.readlines()]
    click.echo(f"part 1: {sum(card.points for card in cards)}")

    click.echo(f"part 2: {sum(count_copies(cards))}")


def count_copies(cards):
    """
    Return a list that contains the number of copies for each card
    """
    copies = [1 for c in cards]

    for card in cards:
        won_cards = card.matching_numbers
        for i in range(card.card_number, card.card_number + won_cards):
            if i >= len(copies):
                break
            copies[i] += copies[card.card_number - 1]

    return copies


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
