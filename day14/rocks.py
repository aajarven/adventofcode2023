class Rocks:
    def __init__(self, symbols, nexts=None):
        self.symbols = self._copy_2darray(symbols)
        if not nexts:
            self._nexts = {}
        else:
            self._nexts = nexts

    def __eq__(self, other):
        if not isinstance(other, Rocks):
            return False
        for l1, l2 in zip(self.symbols, other.symbols):
            for c1, c2 in zip(l1, l2):
                if c1 != c2:
                    return False
        return True

    def __hash__(self):
        return hash(str(self))

    def _copy_2darray(self, arr):
        new_arr = []
        for line in arr:
            new_arr.append(line.copy())
        return new_arr

    @property
    def cycled(self):
        if self in self._nexts:
            return self._nexts[self]

        next_rocks = Rocks(self.symbols, self._nexts)
        for _ in range(4):
            next_rocks.slide_up()
            next_rocks.rotate_clockwise()
        self._nexts[self] = next_rocks
        return next_rocks

    def rotate_clockwise(self):
        new_symbols = []
        for i_new_row in range(len(self.symbols[0])):
            new_row = []
            for i_new_col in range(len(self.symbols)):
                new_row.append(
                    self.symbols[len(self.symbols[0]) - i_new_col - 1][i_new_row]
                )
            new_symbols.append(new_row)
        self.symbols = new_symbols

    def slide_up(self):
        for i_line, line in enumerate(self.symbols[1:], start=1):
            for i_col, symbol in enumerate(line):
                if symbol == "O" and self.symbols[i_line - 1][i_col] == ".":
                    destination_line = i_line - 1
                    while (
                        destination_line > 0
                        and self.symbols[destination_line - 1][i_col] == "."
                    ):
                        destination_line -= 1
                    self.symbols[destination_line][i_col] = "O"
                    line[i_col] = "."

    @property
    def load(self):
        load = 0
        for moment, line in enumerate(self.symbols[::-1]):
            for c in line:
                if c == "O":
                    load += moment + 1
        return load

    def __str__(self):
        return "\n".join(["".join(line) for line in self.symbols])
