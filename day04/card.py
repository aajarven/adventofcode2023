class Card:
    def __init__(self, input_line):
        """
        Create a new card that represents the given line in input
        """
        self.card_number = self._parse_card_number(input_line)
        self.winning_numbers = self._parse_winning_numbers(input_line)
        self.available_numbers = self._parse_available_numbers(input_line)
        self._precalculated_matching_numbers = None

    @property
    def matching_numbers(self):
        """
        Return the number of winning numbers found in the available numbers
        """
        if self._precalculated_matching_numbers:
            return self._precalculated_matching_numbers

        self._precalculated_matching_numbers = 0
        i_winning = 0
        i_available = 0
        while i_winning < len(self.winning_numbers) and i_available < len(
            self.available_numbers
        ):
            current_winning = self.winning_numbers[i_winning]
            current_available = self.available_numbers[i_available]
            if current_winning == current_available:
                self._precalculated_matching_numbers += 1
                i_available += 1
            elif current_winning > current_available:
                i_available += 1
            else:
                i_winning += 1

        return self._precalculated_matching_numbers

    @property
    def points(self):
        """
        The point worth of this card.

        This is 2^n where n is the number of winning numbers found in the available
        numbers.
        """
        if self.matching_numbers == 0:
            return 0
        return 2 ** (self.matching_numbers - 1)

    def _parse_card_number(self, input_line):
        """
        Return the card number extracted from the full input line
        """
        return int(input_line.split(":")[0].strip("Card "))

    def _parse_winning_numbers(self, input_line):
        """
        Return the winning numbers as a sorted list
        """
        winning_number_str = input_line.split(": ")[1].split(" | ")[0]
        return self._str_to_int_list(winning_number_str)

    def _parse_available_numbers(self, input_line):
        """
        Return the available numbers as a sorted list
        """
        available_number_str = input_line.split(": ")[1].split(" | ")[1]
        return self._str_to_int_list(available_number_str)

    def _str_to_int_list(self, string):
        """
        Parse the space-separated integers from a given string and return them sorted
        """
        numbers = [int(number) for number in string.strip().split()]
        numbers.sort()
        return numbers
