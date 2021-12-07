import math
from typing import List, Tuple

import numpy as np

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def parse_input(input_data: List[str]) -> List[int]:
    data = input_data[0]
    return [int(v) for v in data.split(',')]


def calculate_fuel_for_dist(dist: int):
    return dist * (dist + 1) // 2


def cheapest_align(data: List[int], is_expensive=False) -> Tuple[int, int]:
    cheapest = math.inf
    pos = -1
    for i in range(1, max(data) + 1):
        if is_expensive:  # Part 2
            cost = sum(calculate_fuel_for_dist(abs(val-i)) for val in data)
        else:
            cost = sum(abs(val-i) for val in data)
        if cost < cheapest:
            cheapest = cost
            pos = i

    assert pos != -1
    return pos, cheapest


@solution_timer(2021, 7, 1)
def part_one(input_data: List[str]):
    data = parse_input(input_data)
    _, answer = cheapest_align(data)

    if not answer:
        raise SolutionNotFoundException(2021, 7, 1)

    return answer


@solution_timer(2021, 7, 2)
def part_two(input_data: List[str]):
    data = parse_input(input_data)
    _, answer = cheapest_align(data, is_expensive=True)

    if not answer:
        raise SolutionNotFoundException(2021, 7, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 7)
    part_one(data)
    part_two(data)
