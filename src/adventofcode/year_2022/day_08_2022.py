from functools import reduce
import operator as op
from itertools import accumulate
from typing import List

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


def iter_vert(arr: List[List]):

    for col in range(len(arr[0])):
        yield [arr[row][col] for row in range(len(arr))]


def visible_trees(trees: List[List[int]]):

    indices = [list((i, j) for j, _ in enumerate(l)) for i, l in enumerate(trees)]

    border = len(trees) * 2 + (len(trees[0]) - 2) * 2
    seen = set()

    for data in [indices, list(iter_vert(indices))]:
        for line in data[1:-1]:
            from_left = line
            from_right = line[::-1]
            for order in (from_left, from_right):
                # Stores the highest tree encountered until position j
                highest_tree_until_j = accumulate([trees[i][j] for i, j in order[:-1]], max)
                without_border = order[1:-1]
                for ((row, col), height) in zip(without_border, highest_tree_until_j):
                    assert row != 0 and col != 0  # This is a tree on the border
                    tree = trees[row][col]
                    if tree > height and (row != 0 or col != 0):
                        seen.add((row, col, trees[row][col]))

    return border + len(seen)


def scenic_score(row, col, trees):
    score = 1
    house = trees[row][col]
    # Find number of trees smaller than this one on the left
    for i, tree in enumerate(reversed(trees[row][:col]), start=1):
        if tree >= house:
            score *= i
            break
    else:
        score *= i
    # Find number of trees smaller than this one on the right
    assert col + 1 < len(trees[row])
    for i, tree in enumerate(trees[row][col + 1:], start=1):
        if tree >= house:
            score *= i
            break
    else:
        score *= i
    # Find number of trees smaller than this one on the top
    vertical = list(iter_vert(trees))
    for i, tree in enumerate(reversed(vertical[col][:row]), start=1):
        if tree >= house:
            score *= i
            break
    else:
        score *= i
    # Find number of trees smaller than this one on the bottom
    for i, tree in enumerate(vertical[col][row+1:], start=1):
        if tree >= house:
            score *= i
            break
    else:
        score *= i

    return score


@solution_timer(2022, 8, 1)
def part_one(input_data: List[List[int]]):
    answer = visible_trees(input_data)

    if not answer:
        raise SolutionNotFoundException(2022, 8, 1)

    return answer


@solution_timer(2022, 8, 2)
def part_two(input_data: List[List[int]]):
    answer = 0
    for i, line in enumerate(input_data[1:-1], start=1):
        for j, tree in enumerate(line[1:-1], start=1):
            answer = max(scenic_score(i, j, input_data), answer)

    if not answer:
        raise SolutionNotFoundException(2022, 8, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 8)
    data = [[int(t) for t in line] for line in data]
    part_one(data)
    part_two(data)
