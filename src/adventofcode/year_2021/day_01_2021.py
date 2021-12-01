from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


@solution_timer(2021, 1, 1)
def part_one(input_data: List[str]):
    input_data = list(map(int, input_data))
    answer = 0
    for previous, current in zip(input_data[:-1], input_data[1:]):
        if previous < current:
            answer += 1

    if not answer:
        raise SolutionNotFoundException(2021, 1, 1)

    return answer


@solution_timer(2021, 1, 2)
def part_two(input_data: List[str]):
    input_data = list(map(int, input_data))

    windows = []
    for window in zip(input_data[:-1], input_data[1:], input_data[2:]):
        windows.append(sum(window))

    answer = part_one(windows)

    if not answer:
        raise SolutionNotFoundException(2021, 1, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 1)
    part_one(data)
    part_two(data)
