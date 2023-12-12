"""
Advent of code: day 12
"""

from functools import cache

import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    puzzle_strings = input_file.readlines()

    arrangement_sum = 0
    for puzzle_string in puzzle_strings:
        new_arrangements = arrangements(puzzle_string)
        arrangement_sum += new_arrangements
    click.echo(f"part 1: {arrangement_sum}")

    arrangement_sum = 0
    for puzzle_string in puzzle_strings:
        new_arrangements = arrangements(puzzle_string, 5)
        arrangement_sum += new_arrangements
    click.echo(f"part 2: {arrangement_sum}")


def arrangements(puzzle_string, multiplier=1):
    """
    Return the number of arrangements that satisfy the puzzle string.

    Optionally a multiplier can be given for part 2.
    """
    (record_str, group_str) = puzzle_string.split()
    small_constraints = parse_damaged_constraints(record_str)
    small_groups = parse_groups(group_str)

    constraints = (small_constraints + tuple([None])) * (
        multiplier - 1
    ) + small_constraints
    groups = small_groups * multiplier

    return count_arrangements_after(constraints, groups, 0, 0, 0)


@cache
def count_arrangements_after(
    constraints, groups, i_constraints, i_groups, current_block_length
):
    """
    Count the number of arrangements that still satisfy the given `constraints` and
    `groups` when we have already "filled in" springs up to `i_constraints` and the
    next/current group is the `i_groups`th of `groups` and we are currently in a
    `current_block_length` sized group of consecutive broken springs.

    All parameters must be hashable for caching to work, so especially `constraints` and
    `groups` must be tuples instead of lists.
    """

    # Check the last group in completed arrangement
    if i_constraints == len(constraints):
        # Last group ends when the arrangement ends and is the right
        if i_groups == len(groups) - 1 and current_block_length == groups[-1]:
            return 1

        # Last group ended earlier and is the right length
        if i_groups == len(groups) and current_block_length == 0:
            return 1

        # Otherwise not a legal arrangement
        return 0

    found_arrangements = 0
    next_i_constraints = i_constraints + 1

    for next_value in [True, False]:
        # Cannot add value that is not compatible with constraints
        if constraints[i_constraints] not in [next_value, None]:
            continue

        # Broken spring will keep us within the same group but lengthen it
        if next_value is True:
            found_arrangements += count_arrangements_after(
                constraints,
                groups,
                next_i_constraints,
                i_groups,
                current_block_length + 1,
            )

        # Broken string...
        if next_value is False:
            # ... as the first of its block
            if current_block_length == 0:
                found_arrangements += count_arrangements_after(
                    constraints, groups, next_i_constraints, i_groups, 0
                )

            # ... within allowed block length
            elif (
                current_block_length > 0
                and i_groups < len(groups)
                and groups[i_groups] == current_block_length
            ):
                found_arrangements += count_arrangements_after(
                    constraints, groups, next_i_constraints, i_groups + 1, 0
                )

    return found_arrangements


def parse_damaged_constraints(record_str):
    """
    Parse the given broken spring record into a constrain tuple that tells whether a
    given spring is damaged.

    True means damaged, False means intact and None means that data is not available.
    """
    damaged_constraints = []
    for char in record_str:
        match char:
            case ".":
                damaged_constraints.append(False)
            case "#":
                damaged_constraints.append(True)
            case "?":
                damaged_constraints.append(None)
            case _:
                raise ValueError(f"Unexpected constraint {char} encountered")
    return tuple(damaged_constraints)


def parse_groups(group_str):
    """
    Return a tuple with lengths of the consecutive runs of broken springs.
    """
    groups = []
    for substr in group_str.split(","):
        groups.append(int(substr.strip()))
    return tuple(groups)


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
