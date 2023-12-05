import sys

from seed_range import Range


class Mapper:
    """
    A class that can make a single mapping (e.g. seed-to-soil or soil-to-fertilizer).
    """

    def __init__(self, specification_triplets):
        """
        Initialize the class based on given specification.

        specification_triplets: a list of lists, each inner list containing a single map
        """
        self.transformations = {}
        self._populate_transformation_dict(specification_triplets)

    def __str__(self):
        return "\n".join(
            f"Map {trans.start}-{trans.end} to {self.transformations[trans]}-"
            f"{self.transformations[trans]+trans.end-trans.start}"
            for trans in self.transformations
        )

    def _populate_transformation_dict(self, specification_triplets):
        """
        Produces a dict that maps Range -> transformed_start
        """
        for triplet in specification_triplets:
            self.transformations[Range(triplet[1], triplet[2])] = triplet[0]

    def map(self, input_value):
        """
        Return the mapped output value for given input value
        """
        for transformation, destination_start in zip(
            self.transformations.keys(), self.transformations.values()
        ):
            if (
                transformation.start
                <= input_value
                < transformation.start + transformation.length
            ):
                return destination_start + input_value - transformation.start
        return input_value

    def map_range(self, mapped_range):
        """
        Return a list of the new range pair(s) that correspond to given input.

        range_pairs: A list of lists, each inner list having two members (the start of
                     the range and the length of the range)
        """
        new_ranges = []
        while mapped_range:
            found_match = False
            for transformation_range in self.transformations:
                found_match = False
                if transformation_range.contains(mapped_range.start):
                    overlap_length = transformation_range.overlap_length(mapped_range)
                    overlap_start = transformation_range.overlap_start(mapped_range)

                    new_ranges.append(
                        Range(
                            self.transformations[transformation_range]
                            + overlap_start
                            - transformation_range.start,
                            overlap_length,
                        )
                    )
                    mapped_range = Range(
                        mapped_range.start + overlap_length,
                        mapped_range.length - overlap_length,
                    )
                    found_match = True
                    break

            if not found_match:
                earliest_further_match = sys.maxsize
                for transformation_range in self.transformations:
                    if (
                        transformation_range.start > mapped_range.start
                        and (transformation_range.start < earliest_further_match)
                        and transformation_range.start < mapped_range.end
                    ):
                        earliest_further_match = transformation_range.start

                if earliest_further_match != sys.maxsize:
                    new_range = Range(
                        mapped_range.start,
                        earliest_further_match - mapped_range.start,
                    )
                    new_ranges.append(new_range)
                    mapped_range = Range(
                        mapped_range.start + new_range.length,
                        mapped_range.length - new_range.length,
                    )
                else:
                    new_ranges.append(Range(mapped_range.start, mapped_range.length))
                    mapped_range = Range(1, 0)

        return new_ranges
