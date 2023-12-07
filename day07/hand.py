class Hand:
    def __init__(self, input_line):
        self.card_str = input_line.split(" ")[0]
        self.cards = self._cards_from_input(input_line)
        self.bid = self._bid_from_input(input_line)
        self._type = None

    def __str__(self):
        return self.card_str

    def _cards_from_input(self, input_line):
        cards = {}
        for c in input_line[:5]:
            if c not in cards:
                cards[c] = 1
            else:
                cards[c] += 1
        return cards

    def _bid_from_input(self, input_line):
        return int(input_line.split(" ")[1])

    @property
    def type(self):
        """
        Return the type of the hand coded as an integer (bigger is better)
        """
        if self._type:
            return self._type

        self._determine_type()

        return self._type

    def _determine_type(self):
        raise NotImplementedError("Must be implemented in subclasses")

    def __lt__(self, other):
        """
        Comparison (<) operator for hands.

        Hands are primarily ranked using the type of the hand and ties are broken by
        comparing individual cards from left to right.
        """
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False

        for c1, c2 in zip(self.card_str, other.card_str):
            comparison = self._compare_card_chars(c1, c2)
            if comparison > 0:
                return False
            if comparison < 0:
                return True

    def _royal_value_map(self):
        return {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    def _intify_card_char(self, c):
        """
        Make a card character an integer.
        """
        if c.isdigit():
            return int(c)
        return self._royal_value_map()[c]

    def _compare_card_chars(self, c1, c2):
        """
        Return >0 if c1>c2, 0 if c1==c2 and <0 if c1<c2
        """

        i1 = self._intify_card_char(c1)
        i2 = self._intify_card_char(c2)
        return i1 - i2


class Hand1(Hand):
    def _determine_type(self):
        """
        Determine hand type, counting jokers (J) as their own type of card
        """
        sorted_card_counts = sorted(self.cards.values(), reverse=True)

        if sorted_card_counts[0] == 5:
            self._type = 7
        elif sorted_card_counts[0] == 4:
            self._type = 6
        elif sorted_card_counts[0] == 3 and sorted_card_counts[1] == 2:
            self._type = 5
        elif sorted_card_counts[0] == 3:
            self._type = 4
        elif sorted_card_counts[0] == 2 and sorted_card_counts[1] == 2:
            self._type = 3
        elif sorted_card_counts[0] == 2:
            self._type = 2
        else:
            self._type = 1


class Hand2(Hand):
    def _intify_card_char(self, c):
        """
        Make a card character an integer. T, Q, K, A keep their normal values but the
        joker J is the weakest card with value 0.
        """
        if c == "J":
            return 0
        return super()._intify_card_char(c)

    def _royal_value_map(self):
        value_map = super()._royal_value_map()
        value_map["J"] = 1
        return value_map

    def _determine_type(self):
        """
        Determine hand type while taking jokers into account.

        Jokers are separated from the "normal" cards in hand to prevent counting them
        twice, e.g. JJ234 as having two jokers on top the JJ pair. Jokers are not
        checked in all hand types, because if e.g. two pairs had a joker, it would also
        qualify as a three of a kind, which is more valuable.
        """
        if "J" in self.cards:
            jokers = self.cards["J"]
            other_cards = {card: self.cards[card] for card in self.cards if card != "J"}
        else:
            jokers = 0
            other_cards = self.cards

        sorted_card_counts = sorted(other_cards.values(), reverse=True)

        if jokers == 5 or sorted_card_counts[0] + jokers == 5:
            self._type = 7
        elif sorted_card_counts[0] + jokers == 4:
            self._type = 6
        elif sorted_card_counts[0] + jokers == 3 and sorted_card_counts[1] == 2:
            self._type = 5
        elif sorted_card_counts[0] + jokers == 3:
            self._type = 4
        elif sorted_card_counts[0] == 2 and sorted_card_counts[1] == 2:
            self._type = 3
        elif sorted_card_counts[0] + jokers == 2:
            self._type = 2
        else:
            self._type = 1
