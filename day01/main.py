"""
Advent of code: day 01
"""

import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    lines = input_file.readlines()
    click.echo(f"Part 1: {calibration_total(lines)}")
    click.echo(f"Part 2: {spelled_calibration_total(lines)}")


def spelled_calibration_total(lines):
    """
    Return the sum of calibration numbers but allow spelled numbers too
    """
    calibration_total = 0
    for line in lines:
        numberified_line = numberify_numbers(line)
        calibration_total += calibration_number(numberified_line)
    return calibration_total


def numberify_numbers(line):
    """
    Replace all instances of spelled out single-digit numbers with actual digits
    """
    numberified_line = line.replace("one", "o1e")
    numberified_line = numberified_line.replace("two", "t2o")
    numberified_line = numberified_line.replace("three", "t3e")
    numberified_line = numberified_line.replace("four", "4")
    numberified_line = numberified_line.replace("five", "5e")
    numberified_line = numberified_line.replace("six", "6")
    numberified_line = numberified_line.replace("seven", "7")
    numberified_line = numberified_line.replace("eight", "e8t")
    numberified_line = numberified_line.replace("nine", "n9e")
    numberified_line = numberified_line.replace("zero", "0o")
    return numberified_line


def calibration_total(lines):
    """
    Return the sum of calibration numbers for given input lines
    """
    calibration_total = 0
    for line in lines:
        calibration_total += calibration_number(line)
    return calibration_total


def calibration_number(line):
    """
    Return the calibration number (actual digits only) for a line
    """
    return 10 * first_digit(line) + first_digit(reversed(line))


def first_digit(string):
    """
    Return the first digit in the given string
    """
    for character in string:
        try:
            digit = int(character)
        except ValueError:
            pass
        else:
            return digit
    raise ValueError(f"No digit found in line {string}")


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
