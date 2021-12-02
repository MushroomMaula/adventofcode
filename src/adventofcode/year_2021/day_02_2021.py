from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


@solution_timer(2021, 2, 1)
def part_one(input_data: List[str]):
    depth = 0
    horizontal_pos = 0
    for line in input_data:
        command, value = line.split()
        if command == "forward":
            horizontal_pos += int(value)
        elif command == "up":
            depth -= int(value)
        else:
            depth += int(value)

    answer = depth * horizontal_pos
    if not answer:
        raise SolutionNotFoundException(2021, 2, 1)

    return answer


@solution_timer(2021, 2, 2)
def part_two(input_data: List[str]):
    depth = 0
    horizontal_pos = 0
    aim = 0
    for line in input_data:
        command, value = line.split()
        if command == "forward":
            horizontal_pos += int(value)
            depth += aim * int(value)
        elif command == "up":
            aim -= int(value)
        else:
            aim += int(value)

    answer = depth * horizontal_pos
    if not answer:
        raise SolutionNotFoundException(2021, 2, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 2)
    part_one(data)
    part_two(data)
