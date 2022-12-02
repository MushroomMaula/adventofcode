import enum
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class Result(enum.IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class Sign(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def game_result(other: Sign, me: Sign) -> Result:
    """
    Determines the game result of the play
    """

    # Using the encoding Rock=1, Paper=2, Scissors=3 the sign with the higher value wins
    # except if for Rock-Scissors, i.e.
    # Rock < Paper -> Paper wins
    # Rock < Scissor -> For this case however Rock wins
    if other == me:
        return Result.DRAW
    elif me < other:
        if me is Sign.ROCK and other is Sign.SCISSORS:
            return Result.WIN
        else:
            return Result.LOSE
    else:
        if other is Sign.ROCK and me is Sign.SCISSORS:
            return Result.LOSE
        else:
            return Result.WIN


def choose_symbol(other: Sign, expected_result: Result) -> Sign:
    """
    Chooses the correct symbol accoring to the expected result
    """
    if expected_result is Result.DRAW:
        return other
    elif expected_result is Result.WIN:

        if other is not Sign.SCISSORS:
            return Sign(other + 1)
        else:
            return Sign.ROCK
    else:
        if other is not Sign.ROCK:
            return Sign(other - 1)
        else:
            return Sign.SCISSORS


def to_sign(symbol: str) -> Sign:
    if symbol == 'A' or symbol == 'X':
        return Sign.ROCK
    elif symbol == 'B' or symbol == 'Y':
        return Sign.PAPER
    elif symbol == 'C' or symbol == 'Z':
        return Sign.SCISSORS


def to_result(symbol: str) -> Result:
    if symbol == "X":
        return Result.LOSE
    elif symbol == "Y":
        return Result.DRAW
    elif symbol == "Z":
        return Result.WIN


@solution_timer(2022, 2, 1)
def part_one(input_data: List[str]):
    answer = 0

    for line in input_data:
        strategy = line.split()
        assert len(strategy) == 2
        other = to_sign(strategy[0])
        me = to_sign(strategy[1])
        answer += game_result(other, me) + me

    if not answer:
        raise SolutionNotFoundException(2022, 2, 1)

    return answer


@solution_timer(2022, 2, 2)
def part_two(input_data: List[str]):
    answer = 0

    for line in input_data:
        outcome = line.split()
        assert len(outcome) == 2
        other = to_sign(outcome[0])
        expected_result = to_result(outcome[1])
        answer += expected_result + choose_symbol(other, expected_result)

    if not answer:
        raise SolutionNotFoundException(2022, 2, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 2)
    part_one(data)
    part_two(data)
