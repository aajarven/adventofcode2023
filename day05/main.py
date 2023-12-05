"""
Advent of code: day 05
"""

import sys

import click

from mapper import Mapper
from seed_range import Range


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    input_lines = input_file.readlines()
    seeds = seed_ints(input_lines[0])
    mappings = [
        Mapper(spec_lines) for spec_lines in split_to_mapper_specs(input_lines[2:])
    ]

    click.echo(f"part 1: {minimum_soil(seeds, mappings)}")

    seeds = seed_ranges(input_lines[0])
    new_seeds = []
    for mapping in mappings:
        for seed_range in seeds:
            new_seeds += mapping.map_range(seed_range)
        seeds = new_seeds
        new_seeds = []

    click.echo(f"part 2: {min(seed_range.start for seed_range in seeds)}")


def minimum_soil(seeds, mappings):
    minimum_soil = sys.maxsize
    for seed in seeds:
        for mapping in mappings:
            seed = mapping.map(seed)
        if seed < minimum_soil:
            minimum_soil = seed
    return minimum_soil


def seed_ints(seed_line):
    """
    Return a list of seed numbers from given seed specification line
    """
    return [int(substring) for substring in seed_line.strip("seeds: ").split()]


def seed_ranges(seed_line):
    """
    Return a list of ranges corresponding to the numbers from seed spec line
    """
    ranges = []
    spec_numbers = [int(substring) for substring in seed_line.strip("seeds: ").split()]
    for i in range(0, len(spec_numbers), 2):
        ranges.append(Range(spec_numbers[i], spec_numbers[i + 1]))
    return ranges


def split_to_mapper_specs(mapping_lines):
    """
    Iterate over lists of mapping specifications.

    The list of mapping lines for a single transformation are yielded at a time.
    """
    for line in mapping_lines:
        if ":" in line:  # a name for a mapping
            mapping = []
        elif not line.strip():  # empty string => one mapping complete
            yield mapping
        else:
            mapping.append([int(substring) for substring in line.split()])
    yield mapping


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
