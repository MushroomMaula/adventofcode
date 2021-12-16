import enum
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class TypeID(str, enum.Enum):
    LITERAL = '100'
    SUM = '000'
    PRODUCT = '001'
    MIN = '010'
    MAX = '011'
    GREATER_THAN = '101'
    LESS_THAN = '110'
    EQUAL = '111'


class InvalidTypeException(Exception):
    pass


class InvalidLengthTypeException(Exception):
    pass


class Packet:

    @staticmethod
    def to_binary(n: int, padding: int = 4):
        """
        Represents the value in binary format with 0 padding
        """
        return bin(n)[2:].zfill(padding)

    @classmethod
    def from_hex(cls, values: str):
        """
        Interprets the value as a hexadecimal string and creates a binary
        representation, that is feed into the packet
        """
        content = []
        for char in values:
            content.append(int(char, 16))

        return cls(''.join(Packet.to_binary(x) for x in content))

    def __init__(self, content: str):
        self.position = 0
        self.content = content
        self.version_sum = 0
        self.read = 0

    def not_read(self):
        return self.content[self.position:]

    def eat(self, n: int) -> str:
        values = self.content[self.position: self.position + n]
        self.position += n
        self.read += n
        return values

    def parse(self) -> int:
        version = self.eat(3)
        type_id = self.eat(3)
        self.version_sum += int(version, 2)

        if type_id == TypeID.LITERAL:
            value = self._parse_literal()
        else:
            values = self._parse_operator()

            if type_id == TypeID.SUM:
                value = sum(values)

            elif type_id == TypeID.PRODUCT:
                value = 1
                for val in values:
                    value *= val

            elif type_id == TypeID.MIN:
                value = min(values)

            elif type_id == TypeID.MAX:
                value = max(values)

            elif type_id == TypeID.GREATER_THAN:
                assert len(values) == 2
                value = values[0] > values[1]

            elif type_id == TypeID.LESS_THAN:
                assert len(values) == 2
                value = values[0] < values[1]

            elif type_id == TypeID.EQUAL:
                assert len(values) == 2
                value = values[0] == values[1]
            else:
                raise InvalidTypeException(f"{type_id} is not a valid type ID.")

        return value

    def _parse_literal(self) -> int:
        literals = []
        # Take chunks of fives
        chunks = len(self.not_read()) // 5
        for _ in range(chunks):
            literal = self.eat(5)
            # we ignore the first bit
            _id = literal[0]
            literals.append(literal[1:])

            # Indicates that this was the last literal value in the packet, and we are finished with reading
            if _id == '0':
                break

        return int(''.join(literals), 2)

    def _parse_operator(self) -> List[int]:
        length_type_id = self.eat(1)
        if length_type_id == '0':
            bits_in_subpackets = self.eat(15)
            n = int(bits_in_subpackets, 2)
            value = self._parse_subpackets_by_bits(n)
        elif length_type_id == '1':
            num_of_subpackets = self.eat(11)
            n = int(num_of_subpackets, 2)
            value = self._parse_subpackets(n)
        else:
            raise InvalidLengthTypeException(f"{length_type_id} is not a valid length type ID.")

        return value

    def _parse_subpackets_by_bits(self, n: int) -> List[int]:
        """
        Read n bits and parse these as subpacktes
        """
        results = []
        size = self.read + n
        while self.read != size:
            results.append(self.parse())

        return results

    def _parse_subpackets(self, n: int) -> List[int]:
        """
        Reads n subpackets
        """
        results = []
        for _ in range(n):
            results.append(self.parse())

        return results

    def __repr__(self) -> str:
        text = ''
        for i, x in enumerate(self.content):
            if i == self.position:
                text += f"[{x}]"
            else:
                text += x
        return text


@solution_timer(2021, 16, 1)
def part_one(input_data: List[str]):
    p = Packet.from_hex(input_data[0])
    p.parse()
    answer = p.version_sum

    if not answer:
        raise SolutionNotFoundException(2021, 16, 1)

    return answer


@solution_timer(2021, 16, 2)
def part_two(input_data: List[str]):
    p = Packet.from_hex(input_data[0])
    answer = p.parse()

    if not answer:
        raise SolutionNotFoundException(2021, 16, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 16)
    part_one(data)
    part_two(data)
