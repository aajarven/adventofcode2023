"""
Advent of code: day 06
"""

import click

from math import ceil


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    input_lines = input_file.readlines()
    race_durations = extract_numbers(input_lines[0])
    records = extract_numbers(input_lines[1])

    click.echo(f"part 1: {total_winning_ways(race_durations, records)}")

    race_duration = extract_combined_number(input_lines[0])
    record = extract_combined_number(input_lines[1])

    click.echo(f"part 2: {acceleration_margin(race_duration, record)}")


def extract_numbers(input_line):
    return [int(substr) for substr in input_line.split(": ")[1].split()]


def extract_combined_number(input_line):
    return int(input_line.split(": ")[1].replace(" ", ""))


def total_winning_ways(race_durations, records):
    acceleration_margins = [
        acceleration_margin(duration, record)
        for duration, record in zip(race_durations, records)
    ]

    total_winning_ways = 1
    for a_margin in acceleration_margins:
        total_winning_ways = total_winning_ways * a_margin

    return total_winning_ways


def acceleration_margin(race_duration, record):
    """
    Return the number of acceleration times that result in beating the record
    """
    n_winning_acceleration_periods = 0

    optimum_acceleration_period = ceil(race_duration / 2)

    acceleration_period = optimum_acceleration_period
    while distance(race_duration, acceleration_period) > record:
        n_winning_acceleration_periods += 1
        acceleration_period += 1

    acceleration_period = optimum_acceleration_period - 1
    while distance(race_duration, acceleration_period) > record:
        n_winning_acceleration_periods += 1
        acceleration_period -= 1

    return n_winning_acceleration_periods


def distance(race_duration, acceleration_period):
    return (race_duration - acceleration_period) * acceleration_period


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
