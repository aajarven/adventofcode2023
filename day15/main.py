"""
Advent of code: day 15
"""

import click

from lens import Lens


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    steps = input_file.read().strip().split(",")
    lenses = [Lens(step_str) for step_str in steps]

    click.echo(f"part 1: {sum(l.stepstr_hash for l in lenses)}")

    boxes = {}
    for lens in lenses:
        if lens.operation == "=":
            if hash(lens) not in boxes:
                boxes[hash(lens)] = [lens]
            else:
                box = boxes[hash(lens)]
                if lens in box:
                    box[box.index(lens)] = lens
                else:
                    box.append(lens)
        else:
            if hash(lens) in boxes:
                box = boxes[hash(lens)]
                if lens in box:
                    box.remove(lens)

    focusing_power = 0
    for box_number, lenses in boxes.items():
        for i, lens in enumerate(lenses):
            focusing_power += (1 + box_number) * (i + 1) * lens.focal_length

    click.echo(f"part 2: {focusing_power}")


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
