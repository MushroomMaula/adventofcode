import math
from typing import List, Sequence

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def chunks(seq: Sequence, size: int):
    for i in range(size, len(seq)):
        yield i, seq[i - size:i]


def n_unique(packet: str, size=4):
    for i, window in chunks(packet, size):
        if len(set(window)) == size:
            return i


@solution_timer(2022, 6, 1)
def part_one(input_data: List[str]):
    assert len(input_data) == 1
    answer = n_unique(input_data[0])

    if not answer:
        raise SolutionNotFoundException(2022, 6, 1)

    return answer


@solution_timer(2022, 6, 2)
def part_two(input_data: List[str]):
    assert len(input_data) == 1
    answer = n_unique(input_data[0], 14)

    if not answer:
        raise SolutionNotFoundException(2022, 6, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 6)
    part_one(data)
    part_two(data)
