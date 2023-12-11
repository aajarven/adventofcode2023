class Node:
    def __init__(self, specification_line, other_nodes):
        """
        Initialize a new node.

        Each node knows its name and the names of its neighbours, and has a pointer to a
        map containing mapping from name to Node.
        """
        self.name = specification_line.split(" ")[0]
        self.other_nodes = other_nodes

        self.neighbour_names = [
            s.replace("(", "").replace(")", "").replace(",", "")
            for s in specification_line.strip().split(" ")[2:]
        ]

    @property
    def left(self):
        """
        The Node found when going left from this node
        """
        return self.other_nodes[self.neighbour_names[0]]

    @property
    def right(self):
        """
        The Node found when going right from this node
        """
        return self.other_nodes[self.neighbour_names[1]]

    def __str__(self):
        return f"{self.name}: {self.neighbour_names}"
