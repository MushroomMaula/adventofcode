from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def print_screen(screen: List[List[str]]):
    print('\n'.join(''.join(row) for row in screen))
    print()


def execute_instructions(instructions: List[str]):

    screen = [
        [' ' for _ in range(40)] for _ in range(6)
    ]

    signal_strength = 0
    x = 1
    queue = [0]
    cycle = 0
    while queue:

        if cycle < len(instructions):
            details = instructions[cycle]
            instruction, *params = details.split()
            if instruction == "noop":
                queue.append(0)  # Represent noop as 0 add
            elif instruction == "addx":
                assert len(params) == 1
                value = int(params[0])
                queue.append(0)
                queue.append(value)
            else:
                raise ValueError(f"Invalid instruction {instruction}")

        if (cycle-20) % 40 == 0 and cycle <= 220:
            signal_strength += cycle * x

        # Perform action in current cycle
        if queue:
            x += queue.pop(0)

        # Update screen
        crt_row = cycle // 40
        crt_pos = cycle % 40

        if crt_pos == x or crt_pos == (x - 1) or crt_pos == (x + 1):
            screen[crt_row][crt_pos] = '█'

        print_screen(screen)

        cycle += 1
    return signal_strength


@solution_timer(2022, 10, 1)
def part_one_and_two(input_data: List[str]):
    answer = execute_instructions(input_data)

    if not answer:
        raise SolutionNotFoundException(2022, 10, 1)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 10)
    part_one_and_two(data)
