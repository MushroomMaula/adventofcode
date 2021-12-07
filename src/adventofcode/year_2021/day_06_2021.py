import math
from collections import namedtuple
from copy import copy
from decimal import ROUND_HALF_UP, Decimal
from typing import List


import matplotlib.pyplot as plt
import numpy as np

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def parse_inputs(input_data: List[str]) -> List[int]:
    values = input_data[0]
    return [int(timer) for timer in values.split(',')]


def simulate(swarm: List[int], days=80):
    for _ in range(days):
        for i in range(len(swarm)):
            if swarm[i] == 0:
                swarm.append(8)
                swarm[i] = 6
            else:
                swarm[i] -= 1

    return swarm


def simulate_single(fish: int, days=80, is_child=False):

    if days < fish:
        return 0  # even tough we dont reproduce we are still a fish!

    my_children = Decimal((days - fish) / 6).to_integral_value(rounding=ROUND_HALF_UP)
    result = my_children  # 1 for the initial fish
    for i in range(int(my_children)):
        result += simulate_single(8, days-(fish+i*6), is_child=True)

    return result


def fast_simulation(fish: List[int], days=80):
    result = len(fish)
    for f in fish:
        result += simulate_single(f, days)

    return result


@solution_timer(2021, 6, 1)
def part_one(input_data: List[str]):
    fish = parse_inputs(input_data)

    answer = len(simulate(fish))
    if not answer:
        raise SolutionNotFoundException(2021, 6, 1)

    return answer


@solution_timer(2021, 6, 2)
def part_two(input_data: List[str]):
    fish = parse_inputs(input_data)
    answer = len(simulate(fish, 256))
    if not answer:
        raise SolutionNotFoundException(2021, 6, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 6)
    part_one(data)
    part_two(data)
