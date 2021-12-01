from typing import List, cast

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def sonar_sweep(values: List[int]) -> int:
    increasing = 0
    for previous, current in zip(values[:-1], values[1:]):
        if previous < current:
            increasing += 1
    return increasing


@solution_timer(2021, 1, 1)
def part_one(input_data: List[str]):
    sonar_values = cast(List[int], list(map(int, input_data)))
    answer = sonar_sweep(sonar_values)

    if not answer:
        raise SolutionNotFoundException(2021, 1, 1)

    return answer


@solution_timer(2021, 1, 2)
def part_two(input_data: List[str]):
    sonar_values = cast(List[int], list(map(int, input_data)))

    windows = []
    for window in zip(sonar_values[:-1], sonar_values[1:], sonar_values[2:]):
        windows.append(sum(window))

    answer = sonar_sweep(windows)

    if not answer:
        raise SolutionNotFoundException(2021, 1, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 1)
    part_one(data)
    part_two(data)
