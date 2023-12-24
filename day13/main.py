"""
Advent of code: day 13
"""

import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    puzzles = list(read_puzzles(input_file))

    note_number = 0
    for puzzle in puzzles:
        note_number += 100 * rows_above_reflection(puzzle, is_reflection)
        note_number += columns_left_of_reflection(puzzle, is_reflection)
    click.echo(f"Part 1: {note_number}")

    note_number = 0
    for puzzle in puzzles:
        note_number += 100 * rows_above_reflection(puzzle, is_smudged_reflection)
        note_number += columns_left_of_reflection(puzzle, is_smudged_reflection)
    click.echo(f"Part 2: {note_number}")


def is_reflection(puzzle, row):
    """
    Check if the reflection line for given puzzle is below given row
    """
    i = 0
    first_row = row - i
    second_row = row + i + 1
    while True:
        first_row = row - i
        second_row = row + i + 1
        if first_row < 0 or second_row >= len(puzzle):
            return True
        if puzzle[first_row] != puzzle[second_row]:
            return False
        i += 1


def is_smudged_reflection(puzzle, row):
    """
    Check if the smudged reflection line for given puzzle is below given row
    """

    def diff_count(row1, row2):
        diff_count = 0
        for c1, c2 in zip(row1, row2):
            if c1 != c2:
                diff_count += 1
        return diff_count

    smudge_found = False
    i = 0
    first_row = row - i
    second_row = row + i + 1
    while True:
        first_row = row - i
        second_row = row + i + 1
        if first_row < 0 or second_row >= len(puzzle):
            return smudge_found
        dc = diff_count(puzzle[first_row], puzzle[second_row])

        # One difference: might be the smudge if smudge not found yet
        if dc == 1:
            if smudge_found:
                return False
            smudge_found = True

        # More than one difference: cannot be mirror line
        if dc > 1:
            return False
        i += 1


def rows_above_reflection(puzzle, reflection_check):
    """
    Count rows above reflection line in the given puzzle using the given
    reflection check function.
    """
    for row in range(0, len(puzzle) - 1):
        if reflection_check(puzzle, row):
            return row + 1
    return 0


def columns_left_of_reflection(puzzle, reflection_check):
    """
    Count columns left of reflection line.

    This is done by transponing the puzzle input so that leftmost column
    becomes the top row and then using `rows_above_reflection`.
    """
    transponed_puzzle = ["".join(chars) for chars in zip(*puzzle)]
    return rows_above_reflection(transponed_puzzle, reflection_check)


def read_puzzles(input_file):
    current_puzzle = []
    for line in input_file.readlines():
        if not line.strip():
            yield current_puzzle
            current_puzzle = []
        else:
            current_puzzle.append(line.strip())
    if current_puzzle:
        yield current_puzzle


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
