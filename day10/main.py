"""
Advent of code: day XX
"""

import click

from pipe import Pipe, TravelDirection
from empty import Empty


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    pipe_network_chars = parse_pipe_network_chars(input_file.readlines())
    starting_coordinates = find_s(pipe_network_chars)
    start = Pipe(pipe_network_chars, *starting_coordinates)
    loop = pipe_loop(start)
    click.echo(f"part 1: {int(len(loop)/2)}")

    set_start_type(loop)
    immediate_neighbours = left_neighbours(loop)
    all_neighbours = expand_neighbours(immediate_neighbours, loop)

    den_size = len(all_neighbours)
    alternative_den_size = (
        len(pipe_network_chars) * len(pipe_network_chars[0]) - den_size - len(loop)
    )
    click.echo(f"part 2: {den_size} or {alternative_den_size}")


def expand_neighbours(immediate_neighbours, pipe_loop):
    all_neighbours = set()
    queue = immediate_neighbours
    while queue:
        part = queue.pop()
        all_neighbours.add(part)
        for neighbour in part.all_neighbours:
            if neighbour in pipe_loop:
                continue
            if neighbour in all_neighbours:
                continue
            queue.add(neighbour)
    return all_neighbours


def left_neighbours(pipe_loop):
    left_hand_neighbours = set()
    for pipe_part in pipe_loop:
        for neighbour in pipe_part.left_hand_neighbours():
            if neighbour and not neighbour in pipe_loop:
                left_hand_neighbours.add(neighbour)
    return left_hand_neighbours


def empty_spaces(pipe_network_chars, loop):
    empties = []
    for y, char_row in enumerate(pipe_network_chars):
        for x, char in enumerate(char_row):
            if char == ".":
                empties.append(Empty(pipe_network_chars, x, y, loop))
    return empties


def set_start_type(pipe_loop):
    start = pipe_loop[0]
    previous_pipe = pipe_loop[-1]
    next_pipe = pipe_loop[1]

    if previous_pipe.x < next_pipe.x:
        if previous_pipe.y == next_pipe.y:
            start.type = "-"
        elif previous_pipe.y > next_pipe.y:
            start.type = "J"
        else:
            start.type = "7"
    elif previous_pipe.x == next_pipe.x:
        start.type = "|"
    else:
        if previous_pipe.x > next_pipe.x:
            if previous_pipe.y == next_pipe.y:
                start.type = "-"
            elif previous_pipe.y > next_pipe.y:
                start.type = "L"
            else:
                start.type = "F"


def pipe_loop(start):
    loop_pipes = [start]
    p = start
    n = start.pipe_neighbours[0]

    while n != start:
        if p == start:
            if n.x > p.x:
                p.travel_direction = TravelDirection.RIGHT
            elif n.x > p.x:
                p.travel_direction = TravelDirection.LEFT
            elif n.y > p.y:
                p.travel_direction = TravelDirection.DOWN
            else:
                p.travel_direction = TravelDirection.UP
        n.set_travel_direction(p)

        loop_pipes.append(n)
        pp = p
        p = n
        n = n.next(pp)
    return loop_pipes


def parse_pipe_network_chars(input_lines):
    chars = []
    for line in input_lines:
        chars.append([c for c in line.strip()])
    return chars


def find_s(pipe_network_chars):
    for y, char_row in enumerate(pipe_network_chars):
        for x, char in enumerate(char_row):
            if char == "S":
                return (x, y)


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
