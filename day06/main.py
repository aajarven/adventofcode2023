"""
Advent of code: day 06
"""

from math import ceil, floor, sqrt

import click


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
    """
    Extract all space-separated integers that follow a colon in the given line
    """
    return [int(substr) for substr in input_line.split(": ")[1].split()]


def extract_combined_number(input_line):
    """
    Extract a single integer from the substring that follows a colon in the line,
    ignoring spaces
    """
    return int(input_line.split(": ")[1].replace(" ", ""))


def total_winning_ways(race_durations, records):
    """
    Calculate the number of different acceleration times that lead to winning all races
    """
    acceleration_margins = [
        acceleration_margin(duration, record)
        for duration, record in zip(race_durations, records)
    ]

    combinations = 1
    for a_margin in acceleration_margins:
        combinations = combinations * a_margin

    return combinations


def second_degree_zeros(a, b, c):  # pylint: disable=invalid-name
    """
    Solve a second degree equation a*x^2+bx+c=0 and return the solutions in a tuple.

    Assumes that there are always two distinct real solutions. For a downward opening
    parabola the first element of the tuple is always the smaller of the two solutions.
    """
    first_solution = (-1 * b + sqrt(b * b - 4 * a * c)) / (2 * a)
    second_solution = (-1 * b - sqrt(b * b - 4 * a * c)) / (2 * a)
    return (first_solution, second_solution)


def acceleration_margin(race_duration, record):
    """
    Return the number of acceleration times that result in beating the record.

    This is calculated based on the fact that when charging for x ms at the beginning of
    the race, you will travel the distance of (race_duration - x)*x which corresponds to
    -x^2 + race_duration * x. To beat the record, we must achieve
    -x^2 + race_duration * x > record, i.e. -x^2 + race_duration * x - record > 0.

    When the left side is plotted against x, we get a downwards-opening parabola
    (negative term -x^2), so the values of x that satisfy the equation are between the
    zero points. Thus we can solve for them, and count the integers that are found
    between them (including the both end points, if integers).
    """
    zeros = second_degree_zeros(-1, race_duration, -1 * (record + 0.1))
    return floor(zeros[1]) - ceil(zeros[0]) + 1


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
