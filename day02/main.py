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
    lines = input_file.readlines()
    games = parse_games(lines)
    click.echo(f"Part 1: {part1(games)}")
    click.echo(f"Part 2: {part2(games)}")


def part1(games):
    """
    Solve part 1 of te puzzle
    """
    possible_games_sum = 0
    bag_contents = {"red": 12, "green": 13, "blue": 14}
    for i in range(len(games)):  # pylint: disable=consider-using-enumerate
        game_number = i + 1
        if possible(bag_contents, games[i]):
            possible_games_sum += game_number
    return possible_games_sum


def parse_games(lines):
    """
    Get the game information from input lines.

    Returns the games as a list, each list item being a list that contains the
    draws for a single game, each draw being represented as a dict containing
    each color and its count.
    """
    games = []
    for line in lines:
        new_game = []
        game_draws = line.split(":")[1].strip()
        for draw_str in game_draws.split(";"):
            draw = {}
            color_counts = draw_str.strip().split(",")
            for color_count in color_counts:
                count, color = color_count.strip().split(" ")
                draw[color] = int(count)
            new_game.append(draw)
        games.append(new_game)
    return games


def possible(bag_contents, game):
    """
    Return True if given game can be observed from bag_contents

    bag_contents must be a dict with colors and their corresponding number of
    balls, e.g. {"red": 3, "blue": 5}.
    """
    for round_ in game:
        for color in round_:
            if color not in bag_contents:
                return False
            if bag_contents[color] < round_[color]:
                return False
    return True


def part2(games):
    """
    Solve part 2 of the puzzle
    """
    total_power = 0
    for game in games:
        total_power += minimum_bag_power(game)
    return total_power


def minimum_bag_power(game):
    """
    Return the power of the smallest bag that allows the observed draws
    """
    minimum_bag = {}

    for round_ in game:
        for color, count in round_.items():
            if color not in minimum_bag:
                minimum_bag[color] = count
            elif minimum_bag[color] < count:
                minimum_bag[color] = count

    product = 1
    for count in minimum_bag.values():
        product *= count
    return product


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
