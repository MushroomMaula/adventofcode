import math
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


DIRS = {
    'R': (1, 0), 'L': (-1, 0),
    'U': (0, 1), 'D': (0, -1)
}


def vis(knots, size=6,):
    grid = [
        ['·' for _ in range(size)] for _ in range(size*2)
    ]
    for i, k in enumerate(knots):
        x, y = k
        if x < 0:
            x = 2*abs(x)
        if y < 0:
            x = 2*abs(y)
        if grid[y][x] == '·':
            grid[y][x] = str(i)

    print('\n'.join(''.join(l) for l in reversed(grid)))
    print()
    return


def rope_physics(moves, size=2):
    positions = set()
    knots = [[0, 0] for _ in range(size)]

    is_diagonal = lambda x, y: abs(x) == 1 and abs(y) == 1
    is_adjacent = lambda x, y: (abs(x) + abs(y) == 1)
    is_on_top = lambda x, y: abs(x) + abs(y) == 0

    for detail in moves:
        direction, count = detail.split()
        direction = DIRS[direction]

        for _ in range(int(count)):
            knots[0][0] += direction[0]
            knots[0][1] += direction[1]
            for i in range(1, size):
                head = knots[i-1]
                tail = knots[i]

                dx = head[0] - tail[0]
                dy = head[1] - tail[1]

                # Tail does not need to move
                if is_diagonal(dx, dy) or is_adjacent(dx, dy) or is_on_top(dx, dy):
                    continue
                # Head is two steps directly up/down/left or right
                elif abs(dx) == 2 and dy == 0:
                    # Step in the direction of the head
                    knots[i][0] += int(math.copysign(1, dx))
                elif abs(dy) == 2 and dx == 0:
                    knots[i][1] += int(math.copysign(1, dy))
                elif dx != 0 and dy != 0:
                    # Diagonal step in the direction of the head
                    knots[i][0] += math.copysign(1, dx)
                    knots[i][1] += math.copysign(1, dy)
                else:
                    breakpoint()

            positions.add(tuple(knots[-1]))

    return positions


@solution_timer(2022, 9, 1)
def part_one(input_data: List[str]):
    answer = len(rope_physics(input_data))

    if not answer:
        raise SolutionNotFoundException(2022, 9, 1)

    return answer


@solution_timer(2022, 9, 2)
def part_two(input_data: List[str]):
    answer = len(rope_physics(input_data, 10))

    if not answer:
        raise SolutionNotFoundException(2022, 9, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 9)
    part_one(data)
    part_two(data)
