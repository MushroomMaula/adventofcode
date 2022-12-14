import math
from typing import List, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def load_rocks(input_data: List[str]):

    rocks = set()
    for line in input_data:
        coords = [tuple(map(int, c.split(','))) for c in line.split(' -> ')]
        assert len(coords) >= 2
        for start, end in zip(coords[:-1], coords[1:]):
            assert len(start) == 2 and len(end) == 2

            dx = end[0] - start[0]
            dy = end[1] - start[1]
            assert dx == 0 or dy == 0
            for i in range(abs(dx) if dy == 0 else abs(dy)):
                if dx != 0:
                    x = start[0] + int(math.copysign(i+1, dx))
                    y = start[1]
                else:
                    x = start[0]
                    y = start[1] + int(math.copysign(i+1, dy))

                rocks.add((x, y))
                rocks.add(start)
                rocks.add(end)

    return rocks


@solution_timer(2022, 14, 1)
def part_one(input_data: List[str]):
    blocked = load_rocks(input_data)
    last_y = max(blocked, key=lambda x: x[1])[1]
    sand = [500, 0]
    units = 0
    while True:
        # This sand fell below the minimal block, and hence will continue to fall
        if sand[1] >= last_y:
            break

        if (sand[0], sand[1] + 1) in blocked:
            # Test diagonal left
            if (sand[0] - 1, sand[1] + 1) in blocked:
                # Test diagonal right
                if (sand[0] + 1, sand[1] + 1) in blocked:
                    blocked.add(tuple(sand))
                    units += 1
                    sand = [500, 0]
                else:
                    sand[0] += 1
                    sand[1] += 1
            else:
                sand[0] -= 1
                sand[1] += 1
        else:
            sand[1] += 1

    answer = units
    if not answer:
        raise SolutionNotFoundException(2022, 14, 1)

    return answer


@solution_timer(2022, 14, 2)
def part_two(input_data: List[str]):
    blocked = load_rocks(input_data)
    last_y = max(blocked, key=lambda x: x[1])[1]
    floor = last_y + 2
    sand = [500, 0]
    units = 0
    while True:
        if (sand[0], sand[1] + 1) in blocked or sand[1] + 1 == floor:
            # Test diagonal left
            if (sand[0] - 1, sand[1] + 1) in blocked or sand[1] + 1 == floor:
                # Test diagonal right
                if (sand[0] + 1, sand[1] + 1) in blocked or sand[1] + 1 == floor:
                    if sand == [500, 0]:
                        units += 1
                        break
                    else:
                        blocked.add(tuple(sand))
                        units += 1
                        sand = [500, 0]
                else:
                    sand[0] += 1
                    sand[1] += 1
            else:
                sand[0] -= 1
                sand[1] += 1
        else:
            sand[1] += 1

    answer = units

    if not answer:
        raise SolutionNotFoundException(2022, 14, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 14)
    part_one(data)
    part_two(data)
