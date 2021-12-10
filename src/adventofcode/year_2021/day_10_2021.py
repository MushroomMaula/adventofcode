from typing import List, Optional

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


CLOSING_BRACKETS = {'(': ')', '[': ']', '{': '}', '<': '>'}
SYNTAX_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
AUTOCOMPLETE_SCORES = {')': 1, ']': 2, '}': 3, '>': 4}


def get_illegal_char(line: str) -> Optional[str]:
    stack = []
    # We push all opening brackets to the stack and pop closing brackets
    # Thus when we close a bracket if all other brackets inside have been closed
    # the next value on the stack has to be the corresponding opening bracket.
    for char in line:
        if char in '([{<':
            stack.append(char)
        elif char in ')]}>':
            opening_bracket = stack.pop()
            closing_bracket = char
            if closing_bracket != CLOSING_BRACKETS.get(opening_bracket):
                return closing_bracket
        else:
            raise ValueError(f"Invalid character: {repr(char)}")

    return None


def complete_brackets(line: str) -> List[str]:
    stack = []
    for char in line:
        if char in '([{<':
            stack.append(char)
        elif char in ')]}>':
            _opening_bracket = stack.pop()

    # We have read all the characters now we can start completing
    missing = []
    for unmatched_opening in reversed(stack):
        missing.append(CLOSING_BRACKETS.get(unmatched_opening))

    return missing


@solution_timer(2021, 10, 1)
def part_one(input_data: List[str]):
    answer = 0
    for line in input_data:
        illegal_character = get_illegal_char(line)
        if illegal_character is None:
            continue
        else:
            answer += SYNTAX_SCORES[illegal_character]

    if not answer:
        raise SolutionNotFoundException(2021, 10, 1)

    return answer


@solution_timer(2021, 10, 2)
def part_two(input_data: List[str]):
    scores = []
    for line in input_data:
        # Could be optimized by building the stack in another method
        # so we dont have to do this twice, once in get_illegal_char
        # and once in complete_brackets
        if get_illegal_char(line) is not None:
            continue

        score = 0
        for value in complete_brackets(line):
            score *= 5
            score += AUTOCOMPLETE_SCORES[value]
        scores.append(score)

    # Can be optimized by either using median of medians -> O(n)
    # or using insertion from insertion sort above which will also
    # lead to O(n)
    answer = sorted(scores)[len(scores) // 2]
    if not answer:
        raise SolutionNotFoundException(2021, 10, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 10)
    part_one(data)
    part_two(data)
