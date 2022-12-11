import functools
import operator
import re
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


INT_PATTERN = re.compile(r"\d+")


class Monkey:

    def __init__(self, items: List[int], operation: str, value: int, divisor: int, true_to: int, false_to: int):
        self.items = items
        self.operation = operation
        self.parameter = value
        self.div_by = divisor
        self._true_to = true_to
        self._false_to = false_to

        self.inspected_items = 0

    def inspect(self) -> int:
        if self.items:
            self.inspected_items += 1
            return self.items.pop(0)

    def change_worry(self, item: int) -> int:
        if self.operation == '*':
            return item * self.parameter
        elif self.operation == '**':
            return item ** 2
        elif self.operation == '+':
            return item + self.parameter
        else:
            raise ValueError(f"Invalid operation {self.operation}")

    def throw(self, item: int) -> int:
        if item % self.div_by == 0:
            return self._true_to
        else:
            return self._false_to

    def __repr__(self):
        return f"Monkey({self.items}, ∑={self.inspected_items})"


def parse_monkeys(input_data: List[List[str]]) -> List[Monkey]:
    monkeys = []
    for monkey_details in input_data:
        items = [int(item) for item in monkey_details[1][16:].split(', ')]
        op_char = monkey_details[2][21]
        value = monkey_details[2][23:]
        if value == "old":
            op_char = "**"
            value = 2
        else:
            value = int(value)

        divisor = int(monkey_details[3][18:])
        true_to = int(monkey_details[4][25:])
        false_to = int(monkey_details[5][26:])
        monkeys.append(Monkey(items, op_char, value, divisor, true_to, false_to))

    return monkeys


def play(monkeys: List[Monkey], rounds=1, gets_bored=True):

    lcm = functools.reduce(operator.mul, [m.div_by for m in monkeys])

    for round_ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.inspect()
                item = monkey.change_worry(item)
                if gets_bored:
                    item //= 3
                    to = monkey.throw(item)
                else:
                    item %= lcm
                    to = monkey.throw(item)
                monkeys[to].items.append(item)

    return sorted(monkeys, key=operator.attrgetter('inspected_items'), reverse=True)[:2]


@solution_timer(2022, 11, 1)
def part_one(monkeys: List[Monkey]):
    active_monkeys = play(monkeys, 20)
    assert len(active_monkeys) == 2
    answer = active_monkeys[0].inspected_items * active_monkeys[1].inspected_items

    if not answer:
        raise SolutionNotFoundException(2022, 11, 1)

    return answer


@solution_timer(2022, 11, 2)
def part_two(monkeys: List[Monkey]):
    active_monkeys = play(monkeys, 10_000, False)
    assert len(active_monkeys) == 2
    answer = active_monkeys[0].inspected_items * active_monkeys[1].inspected_items

    if not answer:
        raise SolutionNotFoundException(2022, 11, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 11)
    data = [data[i:i+6] for i in range(0, len(data), 7)]
    part_one(parse_monkeys(data))
    part_two(parse_monkeys(data))
