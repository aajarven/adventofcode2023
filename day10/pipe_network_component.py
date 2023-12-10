class PipeNetworkComponent:
    def __init__(self, pipe_network_chars, x, y):
        self.type = pipe_network_chars[y][x]
        self.pipe_network_chars = pipe_network_chars
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x}{self.type}{self.y}")

    def __str__(self):
        return f"{self.type} at row {self.y} position {self.x}"

    def _get_char(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.pipe_network_chars[y][x]
        except IndexError:
            return None

    @property
    def at_edge(self):
        n = [self.char_up, self.char_down, self.char_left, self.char_right]
        return not all(n)

    @property
    def part_up(self):
        char = self.char_up
        if char:
            return PipeNetworkComponent(self.pipe_network_chars, self.x, self.y - 1)
        return None

    @property
    def part_down(self):
        char = self.char_down
        if char:
            return PipeNetworkComponent(self.pipe_network_chars, self.x, self.y + 1)
        return None

    @property
    def part_left(self):
        char = self.char_left
        if char:
            return PipeNetworkComponent(self.pipe_network_chars, self.x - 1, self.y)
        return None

    @property
    def part_right(self):
        char = self.char_right
        if char:
            return PipeNetworkComponent(self.pipe_network_chars, self.x + 1, self.y)
        return None

    @property
    def char_up(self):
        return self._get_char(self.x, self.y - 1)

    @property
    def char_down(self):
        return self._get_char(self.x, self.y + 1)

    @property
    def char_left(self):
        return self._get_char(self.x - 1, self.y)

    @property
    def char_right(self):
        return self._get_char(self.x + 1, self.y)

    @property
    def all_neighbours(self):
        neighbours = []
        for x in [self.x - 1, self.x + 1]:
            if self._get_char(x, self.y):
                neighbours.append(
                    PipeNetworkComponent(self.pipe_network_chars, x, self.y)
                )
        for y in [self.y - 1, self.y + 1]:
            if self._get_char(self.x, y):
                neighbours.append(
                    PipeNetworkComponent(self.pipe_network_chars, self.x, y)
                )
        return neighbours
