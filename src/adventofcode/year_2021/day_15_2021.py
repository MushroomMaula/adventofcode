import heapq
from collections import namedtuple
from typing import List, Tuple
import numpy as np

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day

Node = namedtuple('Node', ['x', 'y', 'risk'])


def parse_map(input_data: List[str]) -> List[List[Node]]:
    graph = []
    for y, line in enumerate(input_data):
        row = []
        for x, risk in enumerate(line):
            row.append(Node(x, y, int(risk)))
        graph.append(row)
    return graph


def enlarge(graph: List[List[Node]]) -> List[List[Node]]:

    risks = np.array([[x.risk for x in row] for row in graph])
    # Create just one column then we will repeat this later
    arr = np.tile(risks, (5, 5))
    size = len(risks)
    for y in range(0, 5 * size, size):
        for x in range(0, 5*size, size):
            arr[y: y + size, x: x+size] += (x+y)//size * np.ones((size, size), dtype=np.int64)
            arr[y: y + size, x: x+size] %= 9

    # Values that were 9 have been replaced by zero
    arr[arr == 0] = 9

    return parse_map(arr.tolist())


def get_neighbors(graph: List[List[Node]], node: Node) -> List[Node]:
    neighbors = []
    if not node.x-1 < 0:
        neighbors.append(graph[node.y][node.x-1])
    if not node.x+1 >= len(graph[0]):
        neighbors.append(graph[node.y][node.x+1])
    if not node.y-1 < 0:
        neighbors.append(graph[node.y-1][node.x])
    if not node.y+1 >= len(graph):
        neighbors.append(graph[node.y+1][node.x])

    return neighbors


def find_path(graph: List[List[Node]]):
    lowest: List[Tuple[int, Node]] = []
    start = graph[0][0]
    goal = graph[-1][-1]
    # We store the risk level of each node
    visited_nodes = {start: 0}
    total_risk, last = (start.risk, start)
    while last != goal:
        for n in get_neighbors(graph, last):
            if n not in visited_nodes:
                result = total_risk + n.risk
                visited_nodes[n] = result
                heapq.heappush(lowest, (result, n))

        total_risk, last = heapq.heappop(lowest)

    return visited_nodes[last] - start.risk


@solution_timer(2021, 15, 1)
def part_one(input_data: List[str]):
    graph = parse_map(input_data)
    answer = find_path(graph)

    if not answer:
        raise SolutionNotFoundException(2021, 15, 1)

    return answer


@solution_timer(2021, 15, 2)
def part_two(input_data: List[str]):
    graph = parse_map(input_data)
    graph = enlarge(graph)
    answer = find_path(graph)

    if not answer:
        raise SolutionNotFoundException(2021, 15, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 15)
    part_one(data)
    part_two(data)
