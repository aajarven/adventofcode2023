class Part:
    """
    Representation of an engine part
    """

    def __init__(self, line, column_start, column_end, value):
        self.line = line
        self.column_start = column_start
        self.column_end = column_end
        self.value = value

    def adjacent_gears(self, engine_array, gears):
        """
        Iterate over adjacent gears
        """
        for row in range(self.line - 1, self.line + 2):
            if row < 0 or row > len(engine_array) - 1:
                continue
            for column in range(self.column_start - 1, self.column_end + 2):
                if column < 0 or column > len(engine_array[0]) - 1:
                    continue
                if engine_array[row][column] == "*":
                    yield gears[(row, column)]


class Gear:
    """
    Representation of a gear in the engine.

    For easy iterating over the pairs of parts connected via a gear, each gear can be
    provided with information about the parts it is adjacent to.
    """

    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.adjacent_parts = []

    def add_adjacent_part(self, part):
        """
        Inform the gear of a Part it is adjacent to
        """
        self.adjacent_parts.append(part)

    @property
    def gear_ratio(self):
        """
        Return the gear ratio of this gear.

        If the gear is not adjacent to two Parts, the ratio is reported as zero (the
        neutral element of sum operation).
        """
        if len(self.adjacent_parts) < 2:
            return 0
        if len(self.adjacent_parts) > 2:
            raise ValueError("Three-way gears are not possible!")
        return self.adjacent_parts[0].value * self.adjacent_parts[1].value
