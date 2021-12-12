from collections import defaultdict, deque
from copy import copy
from typing import List, Tuple, TypeVar, Hashable, Set, DefaultDict, Generic, Optional

from rich.pretty import pprint

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day

T = TypeVar("T", bound=Hashable)


class Graph(Generic[T]):

    @classmethod
    def from_edges(cls, edges: List[Tuple[T, T]]):
        g = cls()
        for src, dest in edges:
            g.insert(src, [dest])

        return g

    def __init__(self):
        self.edges: DefaultDict[T, Set[T]] = defaultdict(set)

    @property
    def vertices(self) -> Set[T]:
        return set(self.edges.keys())

    def insert(self, vertex: T, edges: List[T]):
        """
        Inserts a new node with the given edges
        """
        for val in edges:
            self.edges[vertex].add(val)
            self.edges[val].add(vertex)

    def remove(self, vertex: T):
        """
        Removes the vertex from the graph
        """
        if vertex not in self:
            raise KeyError(f"Graph has no vertex with the value {vertex}")

        remove_from = self.edges[vertex]
        for v in remove_from:
            self.edges[v].remove(vertex)

        self.edges.pop(vertex)

    def __contains__(self, item: T):
        return item in self.edges.keys()

    def __repr__(self):
        return self.edges.__repr__()


class CaveGraph(Graph[str]):

    @classmethod
    def from_edges(cls, edges: List[Tuple[str, str]]):
        g = cls()
        for src, dest in edges:
            g.insert(src, [dest])

        return g

    def __init__(self):
        super().__init__()
        self.paths: Set[str] = set()
        self.current_path = ["start"]

    def simplify(self):
        """
        Removes all lowercase vertices, which cannot be visited
        """
        to_remove = []
        for v, edges in self.edges.items():
            # a small cave that is only connected to other small caves cannot be used
            # in a path
            if v.islower():
                if all(other.islower() for other in edges):
                    to_remove.append(v)

        for v in to_remove:
            self.remove(v)

    def duplicate_small_caves(self):
        # This is probably the stupidest hack ever to solve puzzle 2
        # we just add ever small cave again as a `distinct` node
        # and then check in possible_moves if we already used such a node
        # also we have to remove the '*' when we add the paths else
        # we will get duplicated paths where the cave and its duplicate are
        # just swapped
        for v in copy(self.edges):
            if v.islower() and v not in ("start", "end"):
                self.insert(f"{v}*", list(self.edges[v]))

    def find_paths(self):
        for continuation in self.edges["start"]:
            self.current_path = ["start"]
            visited: Set[str] = set()
            if continuation.islower() and continuation != "end":
                visited.add(continuation)
            self.current_path.append(continuation)
            self.search(continuation, visited)

    def search(self, last: str, visited: Set[str]):
        if last.islower():
            visited.add(last)

        #  filter out all small caves that have been visited
        moves = self.possible_moves(last, visited)
        if len(moves) == 0:
            # If we have no move we cannot reach the end in this path.
            return

        for neighbor in moves:
            self.current_path.append(neighbor)
            if neighbor == "end":
                self.paths.add(','.join(v.replace('*', '') for v in self.current_path))
                self.go_back()  # Remove end from the current path
            else:
                self.search(neighbor, visited.copy())
                self.go_back()

        return

    def possible_moves(self, vertex: str, visited: Set[str]):
        moves = []
        for v in self.edges[vertex]:
            # We do not go back to the start
            if v == "start":
                continue

            elif v.islower() and v in visited:
                continue

            elif any(item.endswith('*') for item in self.current_path) and v.endswith('*'):
                continue
            else:
                moves.append(v)
        return moves

    def go_back(self):
        self.current_path.pop()


def parse_instructions(input_data: List[str]) -> List[Tuple[str, str]]:
    return [(x, y) for x, y in map(lambda x: x.split('-'), input_data)]


@solution_timer(2021, 12, 1)
def part_one(input_data: List[str]):
    graph = CaveGraph.from_edges(parse_instructions(input_data))
    # graph.simplify()
    graph.find_paths()
    answer = len(graph.paths)
    pprint(graph.paths)
    if not answer:
        raise SolutionNotFoundException(2021, 12, 1)

    return answer


@solution_timer(2021, 12, 2)
def part_two(input_data: List[str]):
    graph = CaveGraph.from_edges(parse_instructions(input_data))
    graph.duplicate_small_caves()
    graph.find_paths()
    answer = len(graph.paths)
    pprint(graph.paths)

    if not answer:
        raise SolutionNotFoundException(2021, 12, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 12)
    part_one(data)
    part_two(data)
