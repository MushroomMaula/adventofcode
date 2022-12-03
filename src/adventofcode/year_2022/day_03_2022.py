import string
from functools import reduce
from typing import List, Set, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day

Rucksack = Set[str]

VALUES = {letter: i for i, letter in enumerate(string.ascii_letters, start=1)}


def get_compartments(rucksack: str) -> Tuple[Rucksack, Rucksack]:
    assert len(rucksack) % 2 == 0
    half = len(rucksack) // 2
    first = rucksack[:half]
    second = rucksack[half:]

    return set(first), set(second)


@solution_timer(2022, 3, 1)
def part_one(input_data: List[str]):
    answer = 0
    for line in input_data:
        first, second = get_compartments(line)
        duplicate = first & second
        assert len(duplicate) == 1
        answer += VALUES[duplicate.pop()]

    if not answer:
        raise SolutionNotFoundException(2022, 3, 1)

    return answer


@solution_timer(2022, 3, 2)
def part_two(input_data: List[str]):
    answer = 0

    for i in range(0, len(input_data), 3):
        rucksaecke = input_data[i:i+3]
        group = reduce(lambda x, y: set(x) & set(y), rucksaecke)
        assert len(group) == 1
        answer += VALUES[group.pop()]

    if not answer:
        raise SolutionNotFoundException(2022, 3, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 3)
    part_one(data)
    part_two(data)
