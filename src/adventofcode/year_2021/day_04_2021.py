import itertools
from typing import List, Union, Tuple

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class Piece:
    def __init__(self, value: int):
        self.value = value
        self.marked = False

    def set_marker(self):
        self.marked = True
        
    def __eq__(self, other: Union[int, "Piece"]):
        if isinstance(other, Piece):
            return self.value == other.value
        else:
            return self.value == other

    def __repr__(self):
        return f"{self.value}{'+' if self.marked else '-'}"


class Board:

    def __init__(self, state: List[List[int]]):
        self.state: List[List[Piece]] = [[Piece(v) for v in row] for row in state]
        self._has_won = False

    @classmethod
    def from_text(cls, text: List[str]):
        assert len(text) == 5, "Boards  have to be 5x5"
        state = []
        for line in text:
            state.append([(int(num)) for num in line.split()])
        return cls(state)

    def is_win(self, number: int):
        for row in self.state:
            for value in row:
                if value == number:
                    value.set_marker()

        if self.has_won():
            return True

        return False

    def has_won(self):
        if self._has_won:
            return self._has_won

        for row in self.state:
            if all(piece.marked for piece in row):
                self._has_won = True
                return True

        # check the columns
        for col in range(5):
            if all(self.state[row][col].marked for row in range(5)):
                self._has_won = True
                return True

        return False

    def score(self, won_with):
        unmarked = 0
        for piece in self:
            if not piece.marked:
                unmarked += piece.value
        return won_with * unmarked

    def __repr__(self):
        text = ""
        for row in self.state:
            text += ' '.join(map(str, row)) + '\n'
        return text

    def __iter__(self):
        for row in self.state:
            for piece in row:
                yield piece


def parse_input(input_data: List[str]) -> Tuple[List[int], List[Board]]:
    numbers = [int(num) for num in input_data[0].split(',')]
    boards = []
    text = []
    for line in input_data[2:]:
        if line == '':
            boards.append(Board.from_text(text))
            text = []
        else:
            text.append(line)
    boards.append(Board.from_text(text))
    return numbers, boards


def get_first_winning_board(numbers: List[int], boards: List[Board]):
    for num in numbers:
        for board in boards:
            if board.is_win(num):
                answer = board.score(num)
                return answer


def get_last_winning_board(numbers: List[int], boards: List[Board]) -> int:
    last_winning_score = None
    for num in numbers:
        for board in boards:
            if not board.has_won():
                if board.is_win(num):
                    last_winning_score = board.score(num)

    return last_winning_score


@solution_timer(2021, 4, 1)
def part_one(input_data: List[str]):
    nums, boards = parse_input(input_data)
    answer = get_first_winning_board(nums, boards)

    if not answer:
        raise SolutionNotFoundException(2021, 4, 1)

    return answer


@solution_timer(2021, 4, 2)
def part_two(input_data: List[str]):
    nums, boards = parse_input(input_data)
    answer = get_last_winning_board(nums, boards)

    if not answer:
        raise SolutionNotFoundException(2021, 4, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2021, 4)
    part_one(data)
    part_two(data)
