from collections import deque, Counter
from typing import List, Dict, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def parse_instructions(input_data: List[str]) -> Tuple[str, Dict[str, str]]:
    template = input_data[0]
    rules = {}
    for rule in input_data[1:]:
        if not rule:
            continue
        else:
            condition, _, insertion = rule.partition(' -> ')
            rules[condition] = insertion

    return template, rules


def polymerize(template: str, rules: Dict[str, str], steps=10):
    # Deque seems to be much faster when inserting elements than a list
    #
    after_step = deque(template)

    for _ in range(steps):
        # We have to subtract 1 because a string of length n only contains
        # n-1 consecutive pairs
        for _ in range(len(after_step) - 1):
            first = after_step[0]
            # Move one to the left
            after_step.rotate(-1)
            second = after_step[0]
            key = f"{first}{second}"
            if key in rules:
                # print(f"Found rule {key} -> {rules[key]}")
                # Append after the first key
                after_step.append(rules[key])

        # At the end we are missing one rotation to return the first element
        # to the beginning
        after_step.rotate(-1)

    return ''.join(after_step)


def polymerize_fast(template: str, rules: Dict[str, str], steps=10):
    neighbors: Counter[str] = Counter()
    counter: Counter[str] = Counter(template)
    # add pairs
    for first, second in zip(template[:-1], template[1:]):
        key = f"{first}{second}"
        neighbors[key] += 1

    for _ in range(steps):
        added_neighbors: Counter[str] = Counter()
        for rule, insertion in rules.items():
            if rule in neighbors:
                # every neighbor also should have a counter
                counter[insertion] += neighbors[rule]
                a = rule[0]
                b = rule[1]
                left = f"{a}{insertion}"
                right = f"{insertion}{b}"
                # Update with (possible) new neighbors
                added_neighbors[left] += neighbors[rule]
                added_neighbors[right] += neighbors[rule]
                # We also have to remove the old neighbors
                added_neighbors[rule] -= neighbors[rule]

        neighbors += added_neighbors

    return counter.most_common(1)[0][1] - counter.most_common()[-1][1]


def calculate_answer(polymerization: str):
    counter = Counter(polymerization)
    _, count_most_common = counter.most_common(1)[0]
    _, count_least_common = counter.most_common()[-1]
    return count_most_common - count_least_common


@solution_timer(2021, 14, 1)
def part_one(input_data: List[str]):
    template, rules = parse_instructions(input_data)
    # result = polymerize(template, rules, steps=10)

    answer = polymerize_fast(template, rules, steps=10)
    if not answer:
        raise SolutionNotFoundException(2021, 14, 1)

    return answer


@solution_timer(2021, 14, 2)
def part_two(input_data: List[str]):
    template, rules = parse_instructions(input_data)
    answer = polymerize_fast(template, rules, steps=40)
    if not answer:
        raise SolutionNotFoundException(2021, 14, 10)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 14)
    part_one(data)
    part_two(data)
