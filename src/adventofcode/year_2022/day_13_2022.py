from ast import literal_eval
from collections import deque
from itertools import zip_longest
from functools import cmp_to_key
from typing import List, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def compare(left, right):
    if check_order(left, right):
        return -1
    else:
        return 1


def check_order(left: List, right: List):

    queue = deque(zip(left, right))
    while queue:
        li, ri = queue.popleft()

        if li is None:  # Left ran out of items
            return True
        elif ri is None:  # Right ran out of items
            return False

        if isinstance(li, int) and isinstance(ri, int):
            if li < ri:
                return True
            elif li > ri:
                return False
        elif isinstance(li, int):
            queue.appendleft(([li], ri))
        elif isinstance(ri, int):
            queue.appendleft((li, [ri]))
        else:
            assert isinstance(li, list) and isinstance(ri, list)
            queue.extendleft(reversed(list(zip_longest(li, ri))))

    return len(left) <= len(right)


def parse_packets(input_data: List[str]):
    packets = []
    input_data.append('')
    assert len(input_data) % 3 == 0
    for i in range(0, len(input_data), 3):
        # Get two packets
        left, right, _sep = input_data[i:i + 3]
        assert _sep == ''
        left = literal_eval(left)
        right = literal_eval(right)
        packets.append((left, right))
    return packets


@solution_timer(2022, 13, 1)
def part_one(input_data: List[str]):
    packets = parse_packets(input_data)
    answer = sum(i for i, (left, right) in enumerate(packets, start=1) if check_order(left, right))

    if not answer:
        raise SolutionNotFoundException(2022, 13, 1)

    return answer


@solution_timer(2022, 13, 2)
def part_two(input_data: List[str]):
    packets = [literal_eval(p) for p in input_data if p != '']
    divider_1 = [[2]]
    divider_2 = [[6]]
    packets.append(divider_1)
    packets.append(divider_2)
    correct_order = sorted(packets, key=cmp_to_key(compare))
    answer = (correct_order.index(divider_1) + 1) * (correct_order.index(divider_2) + 1)

    if not answer:
        raise SolutionNotFoundException(2022, 13, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 13)
    part_one(data)
    part_two(data)
