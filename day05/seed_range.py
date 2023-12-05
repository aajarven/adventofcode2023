class Range:
    def __init__(self, start, length):
        self.start = start
        self.length = length

    def __lt__(self, other):
        if not isinstance(other, Range):
            raise ValueError(f"Can't compare Range to {other.__class__}")
        return self.start < other.start

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        return self.start + i

    def __str__(self):
        return f"from {self.start} to {self.end}"

    def __bool__(self):
        return self.length > 0

    @property
    def end(self):
        """
        Return the last position that still belongs to the range
        """
        return self.start + self.length - 1

    def contains(self, position):
        return self.start <= position <= self.end

    def overlaps(self, other_range):
        return (
            other_range.start <= self.end <= other_range.end
            or other_range.start <= self.start <= other_range.end
            or (other_range.start <= self.start and other_range.end >= self.end)
            or (self.start <= other_range.start and self.end >= other_range.end)
        )

    def overlap_end(self, other_range):
        """
        Return the position at which the overlap with the other range ends.

        If there's no overlap, return None.
        """
        if self.overlaps(other_range):
            return min(self.end, other_range.end)
        return None

    def overlap_start(self, other_range):
        """
        Return the position at which the overlap with the other range starts.

        If there's no overlap, return None.
        """
        if self.overlaps(other_range):
            return max(self.start, other_range.start)
        return None

    def overlap_length(self, other_range):
        start = self.overlap_start(other_range)
        end = self.overlap_end(other_range)
        if start and end:
            return end - start + 1
        return None
