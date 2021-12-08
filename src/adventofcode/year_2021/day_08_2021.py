from typing import List, Tuple, Dict, Set

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class Decoder:

    def __init__(self, digits: List[str], results: List[str]):
        self.digits = digits
        self.results = results
        self._encoding: Dict[str, str] = {}
        self._decoded_numbers: Dict[int, Set[str]] = {}

    def _identify_1478(self):
        """
        Identifies the encoding of 1,4,7 and 8 based on its unique
        length
        """
        for value in self.digits:
            length = len(value)
            if length not in (2, 3, 4, 7):
                continue
            elif length == 2:
                self._decoded_numbers[1] = set(value)
            elif length == 3:
                self._decoded_numbers[7] = set(value)
            elif length == 4:
                self._decoded_numbers[4] = set(value)
            else:
                self._decoded_numbers[8] = set(value)

    def _identify_other(self) -> Tuple[List[Set[str]], List[Set[str]]]:
        """
        Returns a tuple with a list containing possible values for 2,3,5 and 0,6,9 respectively
        """
        two_three_five = []
        six_zero_nine = []
        for value in self.digits:
            if len(value) == 5:  # either 2, 3, or 5
                two_three_five.append(set(value))
            elif len(value) == 6:
                six_zero_nine.append(set(value))

        return two_three_five, six_zero_nine

    def _identify_069(self):
        _, zero_six_nine = self._identify_other()
        for x in zero_six_nine:
            for y in zero_six_nine:
                if x == y:
                    continue

                diff = x.difference(y)
                # They all differ in only one letter if this is
                # not the case we got the wrong encodings from self._identify_other
                assert len(diff) == 1
                letter = diff.pop()
                if letter in self._decoded_numbers[1]:
                    # If we have the difference of 9,6 or 0 and 6 we found letter 'c'
                    if len(self._decoded_numbers[4].intersection(x)) == 4:
                        # Only 9 shares all letters with 4 so we can be sure we found 9
                        self._decoded_numbers[9] = x
                        self._decoded_numbers[6] = y
                        self._encoding['c'] = set(letter)
                    else:
                        # We got x=0 and y=6 thus we can calculate d=6\0
                        d = y.difference(x)
                        assert len(d) == 1
                        self._decoded_numbers[0] = x
                        self._encoding['d'] = d.pop()

    def _identify_235(self):
        two_three_five, _ = self._identify_other()
        for x in two_three_five:
            if x.intersection(self._encoding['c']) == set():
                # 5 is the only number (of 2,3,5) that does not contain the encoded letter of c
                self._decoded_numbers[5] = x
            # Ugly hack
            # 3 + the encoded letter of e and 8 are only different in the encoding of letter b
            # 2 on the other hand already contains the encoded letter e, thus the difference of
            # 2 + e and 8 is still b and f
            elif len(self._decoded_numbers[8] - x.union(self._encoding['e'])) == 1:
                self._decoded_numbers[3] = x
                # By the above description this difference is exactly b
                b = (self._decoded_numbers[8] - x.union(self._encoding['e'])).pop()
                self._encoding['b'] = b
            else:
                # Only other possibility
                self._decoded_numbers[2] = x

    def _decode_a(self):
        """
        If the encoding 1 and 7 have been found we can decode
        the letter a based on its
        """
        if any(mandatory not in self._decoded_numbers for mandatory in (1, 7)):
            raise EnvironmentError("Encoding of 1 and 7 is unknown!")
        diff = self._decoded_numbers[7] - self._decoded_numbers[1]
        assert len(diff) == 1, "Invalid encoding for 1 and 7"
        self._encoding['a'] = diff.pop()

    def run(self):
        self._identify_1478()
        self._decode_a()
        self._identify_069()
        self._encoding['e'] = self._decoded_numbers[8].difference(self._decoded_numbers[9])
        self._encoding['f'] = self._decoded_numbers[1].difference(self._encoding['c'])
        self._identify_235()

    def _invert(self):
        """
        Inverts the _decoded_numbers map
        """
        return {frozenset(v): k for k, v in self._decoded_numbers.items()}

    def decode(self, value: str):
        lookup = self._invert()
        return lookup[frozenset(value)]

    def calculate(self) -> int:
        self.run()
        result = ""
        for i, value in enumerate(self.results):
            # each digit is a
            result += str(self.decode(value))

        return int(result)


def parse_input(input_data: List[str]) -> List[Tuple[List[str], List[str]]]:
    values = []
    for line in input_data:
        display, _, result = line.partition('|')
        values.append((display.split(), result.split()))
    return values


def identify_unique_number(value: str) -> int:
    """
    Identifies the corresponding value based on the number
    This only works if the value is of length 2, 3, 4 or 7
    """
    length = len(value)
    if length not in (2, 3, 4, 7):
        raise ValueError("Value can only be identified if it's length is 2, 3, 4 or 7")
    elif length == 2:
        return 1
    elif length == 3:
        return 7
    elif length == 4:
        return 4
    else:
        return 8


@solution_timer(2021, 8, 1)
def part_one(input_data: List[str]):
    data = parse_input(input_data)
    answer = 0
    for values, result in data:
        for digit in result:
            try:
                identify_unique_number(digit)
                answer += 1
            except ValueError:
                continue

    if not answer:
        raise SolutionNotFoundException(2021, 8, 1)

    return answer


@solution_timer(2021, 8, 2)
def part_two(input_data: List[str]):
    data = parse_input(input_data)
    answer = 0
    for values, result in data:
        dec = Decoder(values, result)
        answer += dec.calculate()

    if not answer:
        raise SolutionNotFoundException(2021, 8, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 8)
    part_one(data)
    part_two(data)
