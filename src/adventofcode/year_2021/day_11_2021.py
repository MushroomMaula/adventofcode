import itertools

from dataclasses import dataclass
from typing import List, TypeVar, Tuple, Optional, Iterator, Set

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


T = TypeVar("T")


def flatten(values: List[List[T]]) -> Iterator[T]:
    return itertools.chain.from_iterable(([p for p in row] for row in values))


def parse_inputs(input_data: List[str]) -> List[List["Octopus"]]:
    return [[Octopus(int(c), x, y) for x, c in enumerate(line)] for y, line in enumerate(input_data)]


def get_neighbors(
        array: List[List[T]],
        position: Tuple[int, int],
        n: int = 3,
        fill_value: Optional[T] = None
) -> List[List[Optional[T]]]:
    """
    Returns the values in the box around position.
    """
    x, y = position
    if y < 0 or len(array) <= y:
        raise IndexError(f"{y=} out of bounds.")
    elif x < 0 or len(array[0]) <= x:
        raise IndexError(f"{x=} out of bounds.")

    if n % 2 == 0:
        raise ValueError(f"{n=} cannot be even.")

    # Calculate the 'bounding box' with (x,y) as the center
    half = n // 2
    left_x = x - half
    left_y = y - half
    right_x = x + half
    right_y = y + half

    neighbors = []
    for y in range(left_y, right_y+1):
        if y >= len(array) or y < 0:
            # We are in the first or last row of the array
            neighbors.append([fill_value] * n)
        elif right_x >= len(array):
            # on the right border
            neighbors.append([array[y][x] if x < len(array) else fill_value for x in range(left_x, right_x+1)])
        elif left_x < 0:
            # on the left border
            neighbors.append([array[y][x] if x >= 0 else fill_value for x in range(left_x, right_x+1)])
        else:
            neighbors.append(array[y][left_x: right_x+1])

    return neighbors


@dataclass
class Octopus:
    value: int
    x: int
    y: int

    @property
    def position(self):
        return self.x, self.y

    def reset(self):
        self.value = 0

    def __repr__(self):
        return self.value.__repr__()

    def __hash__(self):
        return self.position.__hash__()


class Swarm:

    def __init__(self, octopi: List[List[Octopus]]):
        self.octopi = octopi
        self.flashes = 0
        self.size = len(list(flatten(octopi)))

    def _find_starting_points(self, exclude: Optional[Set[Octopus]] = None) -> Set[Octopus]:
        """
        Returns the set of coordinates of the octopi with value >= 9
        """
        if exclude is None:
            exclude = set()
        return set((o for o in flatten(self.octopi) if o.value > 9 and o not in exclude))

    def _increment_neighbors(self, octopus: Octopus):
        for neighbor in flatten(get_neighbors(self.octopi, octopus.position)):
            if neighbor is None:
                continue
            neighbor.value += 1

    def simulate(self):
        for octopus in flatten(self.octopi):
            octopus.value += 1

        # We first increase all neighbors of the octopi with a value of 9 or greater.
        # Then we repeat this process until no new octopi has a value of 9 or greater
        starters = self._find_starting_points()
        have_flashed = set()
        while starters != set():
            for octopus in starters:
                self._increment_neighbors(octopus)

            have_flashed.update(starters)
            starters = self._find_starting_points(have_flashed)

        for octopus in have_flashed:
            octopus.value = 0

        self.flashes += len(have_flashed)

        return self.octopi

    def simulate_n(self, n: int):
        for _ in range(n):
            self.simulate()

    def find_synchronisation_step(self):
        previous = int(self.flashes)
        diff = 0
        step = 0
        # If all have flashed self.flashes increased by the size of the swarm
        while diff != self.size:
            previous = self.flashes
            self.simulate()
            step += 1
            diff = self.flashes - previous

        return step

    def __repr__(self):
        text = ""
        for row in self.octopi:
            text += ''.join(map(str, row)) + '\n'
        return text


@solution_timer(2021, 11, 1)
def part_one(input_data: List[str]):
    octopi = parse_inputs(input_data)
    s = Swarm(octopi)
    s.simulate_n(100)
    answer = s.flashes

    if not answer:
        raise SolutionNotFoundException(2021, 11, 1)

    return answer


@solution_timer(2021, 11, 2)
def part_two(input_data: List[str]):
    octopi = parse_inputs(input_data)
    s = Swarm(octopi)
    answer = s.find_synchronisation_step()

    if not answer:
        raise SolutionNotFoundException(2021, 11, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 11)
    part_one(data)
    part_two(data)
