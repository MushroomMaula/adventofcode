import math
import re
from collections import namedtuple
from typing import List, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day

Target = namedtuple('Target', ['lower', 'upper'])
Point = namedtuple('Point', ['x', 'y', 'vel_x', 'vel_y'])
BOUNDS_PATTERN = re.compile("(-?\d+)")


def parse_input(value: str):
    x_1, x_2, y_1, y_2 = map(lambda x: int(x.group()), BOUNDS_PATTERN.finditer(value))
    return Target(lower=(x_1, y_1), upper=(x_2, y_2))


def gauss(n: int) -> int:
    return n * (n+1) // 2


def height_at_max_x(vel_x: int, vel_y: int):
    """
    Assumes vel_x and vel_ y > 0
    """

    return gauss(vel_y) - gauss(vel_y - vel_x)


def solve_gauss(y: int) -> Tuple[float, float]:
    """
    Returns the bound of which value at least is needed to reach that point using
    continued summation.
    This is y = n(n+1) / 2 solved for n
    """
    a = 0.5 + math.sqrt(1/4 + 2*y)
    b = 0.5 - math.sqrt(1/4 + 2*y)
    return a, b


def can_reach_target_straight(target: Target, max_y: int):
    """
    Tests whether we can reach the target zone from the maximum (x, y) coordinates
    with given y velocity at the maximum height
    """
    y = max_y
    # Maximum height is reached when y velocity is zero
    vel_y = 0
    i = 1
    while y >= target.lower[1]:
        if target.lower[1] <= y <= target.upper[1]:
            return i

        y += vel_y
        vel_y -= 1
        i+=1

    return False


def inside_target(target: Target, x: int, y: int):
    return target.lower[0] <= x <= target.upper[0] and target.lower[1] <= y <= target.upper[1]


@solution_timer(2021, 17, 1)
def part_one(input_data: List[str]):
    target = parse_input(input_data[0])
    lower_x = math.ceil(abs(min(solve_gauss(target.lower[0]))))

    last = -math.inf
    # We need to make at least lower_x steps to be in the x boundaries
    # therefore our velocity has to be at least lower_x in order for our
    # maximum to be above the target.
    # We just assume that we have done enough steps with our x velocity so that
    # it is zero, but above the target
    for i in range(lower_x, abs(target.lower[1])):
        height = gauss(i)
        steps = can_reach_target_straight(target, height)
        if steps:
            last = height

    answer = last

    if not answer:
        raise SolutionNotFoundException(2021, 17, 1)

    return answer


@solution_timer(2021, 17, 2)
def part_two(input_data: List[str]):
    target = parse_input(input_data[0])

    velocities = []
    for initial_x in range(target.upper[0]+1):
        for initial_y in range(target.lower[1], abs(target.lower[1])+1):
            x = 0
            y = 0
            vel_x = initial_x
            vel_y = initial_y
            while x <= target.upper[0] and y >= target.lower[1]:
                x += vel_x
                y += vel_y
                if inside_target(target, x, y):
                    velocities.append((initial_x, initial_y))
                    break

                if vel_x != 0:
                    # There is no way the velocity is negative, and we can still reach a target
                    # with positive x coordinates
                    vel_x -= 1
                vel_y -= 1

    answer = len(velocities)
    if not answer:
        raise SolutionNotFoundException(2021, 17, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 17)
    part_one(data)
    part_two(data)
