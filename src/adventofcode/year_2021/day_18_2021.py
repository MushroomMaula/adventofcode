import itertools
import math
from ast import literal_eval
from typing import List, Union

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def explode(source: List[str]) -> bool:
    i = 0
    level = 0
    n = len(source)
    while i < n:
        char = source[i]
        i += 1
        if char == '[':
            level += 1
        elif char == ']':
            level -= 1

        if level > 4:
            # Look where this Snailfish number ends
            end = source.index(']', i)
            content = ''.join(source[i: end])
            left, _, right = content.partition(',')
            # find first number to the left:
            j = i-1
            while j > 0:
                if source[j].isdigit():
                    source[j] = str(int(source[j]) + int(left))
                    break
                j -= 1

            # find first number to the right
            j = end + 1
            while j < n:
                if source[j].isdigit():
                    source[j] = str(int(source[j]) + int(right))
                    break
                j += 1

            # i points at the number, we replace the '[' left of i with zero and remove the rest
            # of the snail fish number
            source[i-1] = '0'
            del source[i: end+1]
            return True

    return False


def split(source: List[str]) -> bool:
    i = 0
    n = len(source)
    while i < n:
        char = source[i]
        i += 1
        if not char.isdigit():
            continue
        # grab the whole number
        j = i
        while source[j].isdigit():
            char += source[j]
            j += 1

        value = int(char)
        if value >= 10:
            half = value / 2
            # in case our number has multiple digits, lets delete all of them except the first one
            del source[i-1:j]
            source.insert(i-1, '[')
            source.insert(i, str(math.floor(half)))
            source.insert(i + 1, ',')
            source.insert(i + 2, str(math.ceil(half)))
            source.insert(i + 3, ']')
            return True

    return False


def add(a: str, b: str) -> str:
    return f"[{a},{b}]"


def sfn_reduce(source: List[str]) -> List[str]:
    explode(source)
    while True:
        while True:
            if not explode(source):
                break

        # No further explosions possible

        if not split(source):
            return source


def group(source: str) -> List[str]:
    """
    Transforms the input into a list where numbers are
    grouped as one element.
    """
    res = []
    i = 0
    n = len(source)
    while i < n:
        char = source[i]
        if not char.isdigit():
            res.append(char)
            i += 1
            continue

        i += 1
        while source[i].isdigit():
            char += source[i]
            i += 1

        res.append(char)

    return res


def calculate(input_data: List[str]) -> str:
    last = input_data[0]
    for b in input_data[1:]:
        source = group(add(last, b))
        last = ''.join(sfn_reduce(source))
    return last


def magnitude(source: List[Union[int, List]]) -> int:
    res = 0
    left, right = source
    if isinstance(left, list):
        res += 3 * magnitude(left)
    else:
        res += 3 * left

    if isinstance(right, list):
        res += 2 * magnitude(right)
    else:
        res += 2 * right

    return res


@solution_timer(2021, 18, 1)
def part_one(input_data: List[str]):
    c = calculate(input_data)
    answer = magnitude(literal_eval(c))
    if not answer:
        raise SolutionNotFoundException(2021, 18, 1)

    return answer


@solution_timer(2021, 18, 2)
def part_two(input_data: List[str]):
    answer = -math.inf
    for pair in itertools.permutations(input_data, 2):
        c = calculate(pair)
        mag = magnitude(literal_eval(c))
        if mag > answer:
            answer = mag

    if not answer:
        raise SolutionNotFoundException(2021, 18, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 18)
    part_one(data)
    part_two(data)
