from typing import List, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def to_section(input_data: List[str]):
    for line in input_data:
        sections = line.split(",")
        sections = [tuple(map(int, s.split('-'))) for s in sections]
        assert len(sections) == 2
        left, right = sections
        yield left, right


def contains_section(left: Tuple[int, int], right: Tuple[int, int]):
    return (left[0] <= right[0] and right[1] <= left[1]) \
                  or (right[0] <= left[0] and left[1] <= right[1])


def overlap(left: Tuple[int, int], right: Tuple[int, int]):
    return left[0] <= right[0] <= left[1] or right[0] <= left[0] <= right[1]


@solution_timer(2022, 4, 1)
def part_one(input_data: List[str]):
    answer = 0

    for left, right in to_section(input_data):
        answer += contains_section(left, right)

    if not answer:
        raise SolutionNotFoundException(2022, 4, 2)

    return answer


@solution_timer(2022, 4, 2)
def part_two(input_data: List[str]):
    answer = 0
    for left, right in to_section(input_data):
        answer += overlap(left, right)

    if not answer:
        raise SolutionNotFoundException(2022, 4, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 4)
    part_one(data)
    part_two(data)
