import math
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def total_per_elf(input_data) -> List[int]:
    totals = []
    total = 0
    for line in input_data:
        if line == "":
            totals.append(total)
            total = 0
        else:
            assert line.isdigit()
            total += int(line)

    # File does not end with an empty line
    totals.append(total)

    return totals


@solution_timer(2022, 1, 1)
def part_one(input_data: List[str]):
    answer = max(total_per_elf(input_data))
    if not answer:
        raise SolutionNotFoundException(2022, 1, 1)

    return answer


@solution_timer(2022, 1, 2)
def part_two(input_data: List[str]):
    calories = sorted(total_per_elf(input_data), reverse=True)
    answer = sum(calories[:3])

    if not answer:
        raise SolutionNotFoundException(2022, 1, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 1)
    part_one(data)
    part_two(data)
