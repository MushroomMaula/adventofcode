from collections import defaultdict
from typing import List, Tuple, Union, Literal, Set, Optional

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class Paper:

    def __init__(self, dots: Optional[Set[Tuple[int, int]]] = None):
        if dots is None:
            dots = set()
        self.dots = dots
        self.max_x: int = 0
        self.max_y: int = 0

    def add_dot(self, x: int, y: int):
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y

        self.dots.add((x, y))

    def _diff_y(self, p: Tuple[int, int], value: int):
        x, y = p
        return 0, abs(value - y)

    def _diff_x(self, p: Tuple[int, int], value: int):
        x, y = p
        return abs(value - x), 0

    def fold(self, along: Literal['x', 'y'], value: int):

        if along == 'x':
            diff = self._diff_x
            self.max_x = value
        elif along == 'y':
            diff = self._diff_y
            self.max_y = value - 1
        else:
            raise ValueError(f"Invalid axis {along}")

        to_remove = []
        new_points = set()
        for x, y in self.dots:
            if along == 'x':
                if x < value:
                    continue
            elif y < value:
                continue
            # let's remove the dots that are getting mirrored
            to_remove.append((x, y))
            dx, dy = diff((x, y), value)
            # project to the point at x-dx, y-dy
            if along == 'x':
                new_points.add((value-dx, y-dy))
            else:
                new_points.add((x-dx, value-dy))

        self.dots.update(new_points)

        for p in to_remove:
            self.dots.remove(p)

    def count(self):
        return len(self.dots)

    def bounds(self) -> Tuple[int, int]:
        return self.max_x, self.max_y

    def __repr__(self):
        rows = [[' ' for _ in range(self.max_x + 1)] for _ in range(self.max_y + 1)]
        for (x, y) in self.dots:
            rows[y][x] = '#'
        return '\n'.join(''.join(v for v in row) for row in rows) + '\n'


def parse_instructions(input_data: List[str]):
    dots = []
    folds: List[Tuple[Literal['x', 'y'], int]] = []
    for line in input_data:
        if not line:
            continue

        if ',' in line:
            a, b = line.split(',')
            dots.append((int(a), int(b)))
        else:
            fold = line[11:]
            axis, value = fold.split('=')
            folds.append((axis, int(value)))

    return dots, folds


@solution_timer(2021, 13, 1)
def part_one(input_data: List[str]):
    dots, folds = parse_instructions(input_data)
    paper = Paper()
    for x, y in dots:
        paper.add_dot(x, y)
    axis, value = folds[0]
    paper.fold(axis, value)
    answer = paper.count()

    if not answer:
        raise SolutionNotFoundException(2021, 13, 1)

    return answer


@solution_timer(2021, 13, 2)
def part_two(input_data: List[str]):
    dots, folds = parse_instructions(input_data)
    paper = Paper()
    for x, y in dots:
        paper.add_dot(x, y)
    for axis, value in folds:
        paper.fold(axis, value)

    answer = '\n' + str(paper) + '\n'

    if not answer:
        raise SolutionNotFoundException(2021, 13, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 13)
    part_one(data)
    part_two(data)
