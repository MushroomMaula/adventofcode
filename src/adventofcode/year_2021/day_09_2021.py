import itertools
import math
import operator
from collections import defaultdict, namedtuple
from pprint import pprint
from typing import List, Tuple, TypeVar, Iterator, Set, Dict

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


T = TypeVar("T")
Point = namedtuple("Point", ["value", "x", "y", "min_neighbor"])


def parse_input(input_data: List[str]) -> List[List[Tuple[int, int, int]]]:
    field = []
    for y, line in enumerate(input_data):
        field.append([(int(c), x, y) for x, c in enumerate(line) if c.isdigit()])
    return field


def create_heightmap(input_data: List[List[Tuple[int, int, int]]]) -> List[List[Point]]:
    """
    Create a 2D-array of Points with minimal neighbor already stored
    """
    heightmap = []
    for row in input_data:
        points = []
        for value, x, y in row:
            # dummy values for comparison
            left = (math.inf, -1, -1)
            right = (math.inf, -1, -1)
            above = (math.inf, -1, -1)
            below = (math.inf, -1, -1)
            if 0 < x:
                left = row[x - 1]
            if x < len(row)-1:
                right = row[x + 1]

            if 0 < y:
                above = input_data[y - 1][x]
            if y < len(input_data) - 1:
                below = input_data[y + 1][x]

            # find the minimal neighbor
            minimal_neighbor = min([left, right, above, below], key=operator.itemgetter(0))

            if value < minimal_neighbor[0]:
                p = Point(value, x, y, None)
                points.append(p)
            else:
                p = Point(value, x, y, minimal_neighbor[1:])
                points.append(p)

        heightmap.append(points)

    return heightmap


def flatten(values: List[List[T]]) -> Iterator[T]:
    return itertools.chain.from_iterable([[p for p in row] for row in values])


def find_minima(heightmap: List[List[Point]]) -> List[Point]:
    return [p for p in flatten(heightmap) if p.min_neighbor is None]


def find_basins(heightmap: List[List[Point]]):
    to_visit = set([p for p in flatten(heightmap) if p.value != 9])

    basins: defaultdict[Point, Set[Point]] = defaultdict(set)
    path = set()
    node = to_visit.pop()
    path.add(node)
    # Maps visited points to its minima
    visited: Dict[Point, Point] = {}
    while to_visit != set():
        # We found a minimum
        if node.min_neighbor is None:
            basins[node].update(path)
            for p in path:
                visited[p] = node
            node = to_visit.pop()
            path.clear()
            path.add(node)
        else:
            # Choose the next node based on the minimal neighbor
            # if this neighbor has already been visited we can look up
            # it's corresponding minimum and add the current path to it
            # We do this until we find a node we have not visited yet
            x, y = node.min_neighbor
            node = heightmap[y][x]
            path.add(node)
            while node in visited and to_visit != set():
                minima = visited[node]
                basins[minima].update(path)
                for p in path:
                    visited[p] = minima
                node = to_visit.pop()
                path.clear()
                path.add(node)

    return basins


@solution_timer(2021, 9, 1)
def part_one(input_data: List[str]):
    values = parse_input(input_data)
    heightmap = create_heightmap(values)
    minima = find_minima(heightmap)
    risk_levels = [m.value + 1 for m in minima]
    answer = sum(risk_levels)

    if not answer:
        raise SolutionNotFoundException(2021, 9, 1)

    return answer


@solution_timer(2021, 9, 2)
def part_two(input_data: List[str]):
    values = parse_input(input_data)
    heightmap = create_heightmap(values)
    basins = find_basins(heightmap)
    sizes = sorted((len(basin) for basin in basins.values()), reverse=True)
    # Multiply the number of items of the three largest basins
    a, b, c, *_ = sizes

    answer = a * b * c
    if not answer:
        raise SolutionNotFoundException(2021, 9, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 9)
    part_one(data)
    part_two(data)
