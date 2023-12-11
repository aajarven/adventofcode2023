"""
Advent of code: day 08
"""


import math

import click

from node import Node


@click.command()
@click.argument("input_file", type=click.File("r"))
def solve(input_file):
    """
    Solve the day's exercise.
    """
    input_lines = input_file.readlines()
    directions = input_lines[0].strip()

    nodes = {}
    for input_line in input_lines[2:]:
        new_node = Node(input_line, nodes)
        nodes[new_node.name] = new_node

    first_node_name = "AAA"

    click.echo(f"part 1: {steps_to_zzz(directions, nodes[first_node_name])}")

    initial_nodes = [node for node in nodes.values() if node.name.endswith("A")]
    click.echo(f"part 2: {steps_to_traverse_all_to_xxz(directions, initial_nodes)}")


def steps_to_zzz(instructions, initial_node):
    steps = 0
    current_node = initial_node

    while current_node.name != "ZZZ":
        if instructions[steps % len(instructions)] == "R":
            current_node = current_node.right
        else:
            current_node = current_node.left
        steps += 1
    return steps


def steps_to_traverse_all_to_xxz(instructions, initial_nodes):
    """
    Return the number of steps it takes for all ghosts to be simultaneously at **Z.

    The generic solution would require that we take into account the possibility that
    each ghost has multiple Z-ending nodes in their cycle, or that there might be extra
    steps before the ghost enters the cycle. Inspecting the input proved that that is
    not the case, so the more advanced functionality was not included.
    """
    current_nodes = initial_nodes.copy()

    cycle_lengths = [None] * len(current_nodes)

    steps = 0
    while not all(cycle_lengths):
        instruction = instructions[steps % len(instructions)]
        for i, node in enumerate(current_nodes):
            if node.name.endswith("Z") and not cycle_lengths[i]:
                cycle_lengths[i] = steps
            if instruction == "R":
                current_nodes[i] = node.right
            else:
                current_nodes[i] = node.left

        steps += 1

    return math.lcm(*cycle_lengths)


if __name__ == "__main__":
    solve()  # pylint: disable=no-value-for-parameter
