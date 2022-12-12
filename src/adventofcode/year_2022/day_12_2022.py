import math
import string
from collections import defaultdict
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


HEIGHT = {char: i for i, char in enumerate(string.ascii_lowercase)}
HEIGHT.update({"S": HEIGHT['a'], 'E': HEIGHT['z']})


def make_map(input_data: List[str]):
    start = None
    end = None
    height_map = {}
    for i, line in enumerate(input_data):
        for j, position in enumerate(line):

            if position == "S":
                start = (i, j)
            elif position == 'E':
                end = (i, j)

            height_map[(i, j)] = set()

            # Add all possible movements as neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni = i + dx
                nj = j + dy
                # Is a possible neighbor
                if 0 <= ni < len(input_data) and 0 <= nj < len(line):
                    neighbor = input_data[ni][nj]
                    dz = HEIGHT[neighbor] - HEIGHT[position]

                    if dz <= 1:  # At most one higher
                        height_map[(i, j)].add((ni, nj))

    return start, end, height_map


def shortest_path(start, end, graph, weight=1):
    visited = set(start)
    path_length = {node: math.inf for node in graph.keys()}
    path_length[start] = 0
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node == end:
            return path_length[node]

        neighbors = graph[node]
        for n in neighbors:
            if n in visited:
                continue

            visited.add(n)
            if path_length[node] + weight <= path_length[n]:
                path_length[n] = path_length[node] + weight
                queue.append(n)

    return math.inf  # No path found


@solution_timer(2022, 12, 1)
def part_one(input_data: List[str]):
    start, end, graph = make_map(input_data)
    answer = shortest_path(start, end, graph)

    if not answer:
        raise SolutionNotFoundException(2022, 12, 1)

    return answer


@solution_timer(2022, 12, 2)
def part_two(input_data: List[str]):
    start, end, graph = make_map(input_data)
    answer = shortest_path(start, end, graph)
    for i, j in graph:
        if input_data[i][j] == 'a':
            answer = min(answer, shortest_path((i, j), end, graph))

    if not answer:
        raise SolutionNotFoundException(2022, 12, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 12)
    part_one(data)
    part_two(data)
