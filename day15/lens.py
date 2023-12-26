class Lens:
    def __init__(self, step_str):
        self.str = step_str
        if "=" in step_str:
            self.operation = "="
            self.focal_length = int(step_str[-1])
        elif "-" in step_str:
            self.operation = "-"
        else:
            raise ValueError("Unexpected operator")
        self.label = step_str.split(self.operation)[0]

    def __hash__(self):
        hash_ = 0
        for char in self.label:
            hash_ += ord(char)
            hash_ *= 17
            hash_ %= 256
        return hash_

    @property
    def stepstr_hash(self):
        hash_ = 0
        for char in self.str:
            hash_ += ord(char)
            hash_ *= 17
            hash_ %= 256
        return hash_

    def __eq__(self, other):
        return other.label == self.label
