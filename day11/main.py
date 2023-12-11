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
    input_lines = [l.strip() for l in input_file.readlines()]
    galaxies = find_galaxies(input_lines)
    expanded_rows = find_expanded_rows(input_lines)
    expanded_columns = find_expanded_columns(input_lines)

    total_distance = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total_distance += distance(
                g1, g2, expanded_rows, expanded_columns, expansion_multiplier=2
            )

    click.echo(f"part 1: {total_distance}")

    total_distance = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total_distance += distance(
                g1, g2, expanded_rows, expanded_columns, expansion_multiplier=1000000
            )

    click.echo(f"part 2: {total_distance}")


def distance(g1, g2, expanded_rows, expanded_columns, expansion_multiplier):
    """
    Calculate the distance between galaxies g1 and g2 in an expanding space.
    """

    def n_elements_in_list_between(value1, value2, list_):
        """
        Determine the number of expanded rows/columns between two positions
        """
        if value2 < value1:  # simplify calculations by ensuring that value1 <= value2
            (value1, value2) = (value2, value1)
        found = 0
        for value in list_:
            if value1 < value < value2:
                found += 1
            if value > value2:
                break
        return found

    taxicab = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    extra_columns = n_elements_in_list_between(g1[0], g2[0], expanded_columns)
    extra_rows = n_elements_in_list_between(g1[1], g2[1], expanded_rows)

    return (
        taxicab
        + extra_rows * expansion_multiplier
        + extra_columns * expansion_multiplier
        # prevent adding 11 columns/rows when multiplying by 10 (one original +10 extra)
        - extra_columns
        - extra_rows
    )


def find_galaxies(input_lines):
    """
    Return a list of galaxies, each galaxy represented as tuple of coordinates.

    Expansion not included at this point.
    """
    galaxies = []
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))
    return galaxies


def find_expanded_rows(input_lines):
    """
    Return indexes of galaxyless rows
    """
    expanded_rows = []
    for y, line in enumerate(input_lines):
        if all(c == "." for c in line):
            expanded_rows.append(y)
    return expanded_rows


def find_expanded_columns(input_lines):
    """
    Return indexes of galaxyless columns
    """
    expanded_columns = []
    for x in range(len(input_lines[0])):
        expanding = True
        for line in input_lines:
            if line[x] != ".":
                expanding = False
        if expanding:
            expanded_columns.append(x)
    return expanded_columns


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
