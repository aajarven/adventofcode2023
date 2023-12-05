class Mapper:
    """
    A class that can make a single mapping (e.g. seed-to-soil or soil-to-fertilizer).
    """

    def __init__(self, specification_triplets):
        """
        Initialize the class based on given specification.

        specification_triplets: a list of lists, each inner list containing a single map
        """
        self.specs = specification_triplets

    def map(self, input_value):
        """
        Return the mapped output value for given input value
        """
        for spec in self.specs:
            if spec[1] <= input_value < spec[1] + spec[2]:
                return spec[0] + input_value - spec[1]
        return input_value
