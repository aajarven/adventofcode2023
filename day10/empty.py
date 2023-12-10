from pipe_network_component import PipeNetworkComponent
from pipe import Pipe


class Empty(PipeNetworkComponent):
    def __init__(self, pipe_network_chars, x, y, pipe_loop):
        self.pipe_loop = pipe_loop
        super().__init__(pipe_network_chars, x, y)

    @property
    def reaches_outside(self):
        visited = set()
        queue = set([self])
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            visited.add(current)

            if current.at_edge:
                return True

            if current in self.pipe_loop:
                current = Pipe(self.pipe_network_chars, current.x, current.y)
                if current.is_corner:
                    neighbours = current.pipe_neighbours + current.all_neighbours
                else:
                    neighbours = current.pipe_neighbours
            else:
                neighbours = current.all_neighbours

            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.add(neighbour)
        return False
