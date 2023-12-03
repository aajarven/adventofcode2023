"""
Advent of code: day 03
"""

import click


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    engine_array = read_to_array(input_file)
    click.echo(f"part 1: {part_number_sum(engine_array)}")


def part_number_sum(engine_array):
    """
    Return the sum of all part numbers in given array
    """

    part_number_sum = 0

    def check_and_add(
        current_number, engine_array, line_number, number_start, number_end
    ):
        """
        Check if we have just seen a number that is part of the engine, and add
        it to part_number sum if we have
        """
        if current_number:
            if is_engine_part(engine_array, line_number, number_start, number_end):
                nonlocal part_number_sum
                part_number_sum += int(current_number)

    for line_number in range(len(engine_array)):
        line = engine_array[line_number]
        current_number = ""
        number_start = None
        for column_number in range(len(line)):
            current_char = line[column_number]
            if current_char.isdigit():
                current_number += current_char
                if not number_start:
                    number_start = column_number
            else:
                check_and_add(
                    current_number,
                    engine_array,
                    line_number,
                    number_start,
                    column_number - 1,
                )
                current_number = ""
                number_start = None

            # line ending, add current number even if haven't seen non-digit
            if column_number == len(line) - 1:
                check_and_add(
                    current_number,
                    engine_array,
                    line_number,
                    number_start,
                    column_number,
                )

    return part_number_sum


def is_engine_part(engine_array, line_number, number_start, number_end):
    """
    Return True if a symbol is found adjacent to the given number coordinates.

    We also check the number itself because that simplifies the code, but it
    doesn't matter because digits don't count as symbols.
    """
    for row in range(line_number - 1, line_number + 2):
        for column in range(number_start - 1, number_end + 2):
            if is_symbol(engine_array, row, column):
                return True
    return False


def is_symbol(engine_array, line, column):
    """
    Return True if given coordinates in the array contain something that isn't
    a period or a digit. False is also returned for coordinates outside the
    engine.
    """
    if line < 0 or line > len(engine_array) - 1:
        return False
    if column < 0 or column > len(engine_array[0]) - 1:
        return False

    char = engine_array[line][column]

    if char.isdigit():
        return False
    if char == ".":
        return False

    return True


def read_to_array(input_file):
    """
    Read given input file to a 2D array of characters.

    The indexing goes array[line][column].
    """
    arr = []
    for line in input_file.readlines():
        line_arr = []
        for char in line.strip():
            line_arr.append(char)
        arr.append(line_arr)
    return arr


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
