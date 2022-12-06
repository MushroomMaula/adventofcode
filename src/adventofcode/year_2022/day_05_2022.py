import math
from collections import deque
from typing import List, Tuple
import re

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


STACK_PATTERN = re.compile(r"(\w)")
COMMAND_PATTERN = re.compile(r"(\d+)")


def parse(input_data: List[str]):

    stacks: List[deque] = []
    moves: List[Tuple[int, int, int]] = []
    for line in input_data:

        if line.startswith("move"):
            instructions = [int(i) for i in re.findall(COMMAND_PATTERN, line)]
            assert len(instructions) == 3
            moves.append(tuple(instructions))
        else:
            if "[" not in line:
                continue

            for match in re.finditer(STACK_PATTERN, line):
                idx = math.ceil(match.start() / 4)
                # Allocate stacks
                if idx > len(stacks):
                    for _ in range(idx - len(stacks)):
                        stacks.append(deque())
                # Switch to 0 based indexing
                idx -= 1
                assert idx < len(stacks)
                assert len(match.group()) == 1
                stacks[idx].appendleft(match.group()[0])

    return stacks, moves


def simulate_single(stacks: List[deque], moves: List[Tuple[int, int, int]]):
    for N, source, dest in moves:
        # Stacks are 1 indexed
        assert 0 < source <= len(stacks) and 0 < dest <= len(stacks)
        for _ in range(N):
            crate = stacks[source-1].pop()
            stacks[dest-1].append(crate)
    return stacks


def simulate_9001(stacks: List[deque], moves: List[Tuple[int, int, int]]):
    for N, source, dest in moves:
        # Stacks are 1 indexed
        assert 0 < source <= len(stacks) and 0 < dest <= len(stacks)
        crates = deque()
        for _ in range(N):
            crate = stacks[source-1].pop()
            crates.appendleft(crate)

        stacks[dest - 1].extend(crates)
    return stacks


@solution_timer(2022, 5, 1)
def part_one(input_data: List[str]):
    answer = ""
    stacks, moves = parse(input_data)
    simulate_single(stacks, moves)
    for stack in stacks:
        answer += stack[-1]

    if not answer:
        raise SolutionNotFoundException(2022, 5, 1)

    return answer


@solution_timer(2022, 5, 2)
def part_two(input_data: List[str]):
    answer = ""
    stacks, moves = parse(input_data)
    simulate_9001(stacks, moves)
    for stack in stacks:
        answer += stack[-1]

    if not answer:
        raise SolutionNotFoundException(2022, 5, 2)

    return answer


if __name__ == '__main__':
    with open("../inputs/2022/day_05.txt", "r") as f:
        data = f.readlines()
    part_one(data)
    part_two(data)
