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
    measurement_sequences = [parse_sequence(line) for line in input_file.readlines()]

    next_measurements = [
        extrapolated_value(measurement_sequence)
        for measurement_sequence in measurement_sequences
    ]
    click.echo(f"part 1: {sum(next_measurements)}")

    first_measurements = [
        extrapolated_value(measurement_sequence[::-1])
        for measurement_sequence in measurement_sequences
    ]
    click.echo(f"part 2: {sum(first_measurements)}")


def extrapolated_value(measurement_sequence):
    """
    Extrapolate the next value in the sequence.

    We recursively calculate the successive "derivatives" until we reach zero,
    at which point we get the next measurement by summing up the last item in
    each list over the Nth derivatives.
    """
    if any(measurement != 0 for measurement in measurement_sequence):
        diffs = []
        for i in range(len(measurement_sequence) - 1):
            diffs.append(measurement_sequence[i + 1] - measurement_sequence[i])
        return measurement_sequence[-1] + extrapolated_value(diffs)
    return 0


def parse_sequence(line):
    return [int(s) for s in line.split()]


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
