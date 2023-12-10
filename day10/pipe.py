from pipe_network_component import PipeNetworkComponent

from enum import Enum, auto


class TravelDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Pipe(PipeNetworkComponent):
    def __init__(self, pipe_network_chars, x, y, travel_direction=None):
        self.travel_direction = travel_direction
        super().__init__(pipe_network_chars, x, y)

    def set_travel_direction(self, previous):
        match previous.travel_direction:
            case TravelDirection.LEFT:
                match self.type:
                    case "-":
                        self.travel_direction = TravelDirection.LEFT
                    case "L":
                        self.travel_direction = TravelDirection.UP
                    case "F":
                        self.travel_direction = TravelDirection.DOWN
                    case _:
                        raise ValueError("Unhandled travel type")

            case TravelDirection.RIGHT:
                match self.type:
                    case "-":
                        self.travel_direction = TravelDirection.RIGHT
                    case "J":
                        self.travel_direction = TravelDirection.UP
                    case "7":
                        self.travel_direction = TravelDirection.DOWN
                    case _:
                        raise ValueError("Unhandled travel type")

            case TravelDirection.UP:
                match self.type:
                    case "|":
                        self.travel_direction = TravelDirection.UP
                    case "7":
                        self.travel_direction = TravelDirection.LEFT
                    case "F":
                        self.travel_direction = TravelDirection.RIGHT
                    case _:
                        raise ValueError("Unhandled travel type")
            case TravelDirection.DOWN:
                match self.type:
                    case "|":
                        self.travel_direction = TravelDirection.DOWN
                    case "L":
                        self.travel_direction = TravelDirection.RIGHT
                    case "J":
                        self.travel_direction = TravelDirection.LEFT
                    case _:
                        raise ValueError("Unhandled travel type")

    def left_hand_neighbours(self):
        if not self.travel_direction:
            raise RuntimeError(
                "travel direction must be set before determining left hand neighbours"
            )
        match self.travel_direction:
            case TravelDirection.UP:
                match self.type:
                    case "|":
                        return [self.part_left]
                    case "L":
                        return [self.part_down, self.part_left]
                    case "J":
                        return []
                    case _:
                        raise ValueError("Unexpected type/direction combination")
            case TravelDirection.DOWN:
                match self.type:
                    case "|":
                        return [self.part_right]
                    case "F":
                        return []
                    case "7":
                        return [self.part_up, self.part_right]
                    case _:
                        raise ValueError("Unexpected type/direction combination")
            case TravelDirection.LEFT:
                match self.type:
                    case "-":
                        return [self.part_down]
                    case "J":
                        return [self.part_right, self.part_down]
                    case "7":
                        return []
                    case _:
                        raise ValueError("Unexpected type/direction combination")
            case TravelDirection.RIGHT:
                match self.type:
                    case "-":
                        return [self.part_right]
                    case "L":
                        return []
                    case "F":
                        return [self.part_left, self.part_up]
                    case _:
                        raise ValueError("Unexpected type/direction combination")

    def next(self, previous):
        neighbours = self.pipe_neighbours
        if neighbours[0] == previous:
            return neighbours[1]
        return neighbours[0]

    @property
    def at_edge(self):
        if self.type in ["|", "-"]:
            return False
        return super().at_edge

    @property
    def is_corner(self):
        return self.type in ["F", "7", "J", "L"]

    @property
    def pipe_neighbours(self):
        neighbours = []

        def add_top():
            if self.char_up in ["|", "7", "F", "S"]:
                neighbours.append(Pipe(self.pipe_network_chars, self.x, self.y - 1))

        def add_bottom():
            if self.char_down in ["|", "J", "L", "S"]:
                neighbours.append(Pipe(self.pipe_network_chars, self.x, self.y + 1))

        def add_left():
            if self.char_left in ["-", "L", "F", "S"]:
                neighbours.append(Pipe(self.pipe_network_chars, self.x - 1, self.y))

        def add_right():
            if self.char_right in ["-", "J", "7", "S"]:
                neighbours.append(Pipe(self.pipe_network_chars, self.x + 1, self.y))

        match self.type:
            case "|":
                add_top()
                add_bottom()
            case "-":
                add_left()
                add_right()
            case "L":
                add_top()
                add_right()
            case "J":
                add_left()
                add_top()
            case "7":
                add_left()
                add_bottom()
            case "F":
                add_right()
                add_bottom()
            case "S":
                add_top()
                add_bottom()
                add_left()
                add_right()
        return neighbours
