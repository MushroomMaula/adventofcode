import math
from typing import List, Optional, Union, Set, Tuple, Callable, Dict, Generator

from adventofcode.util.exceptions import SolutionNotFoundException
from adventofcode.util.helpers import solution_timer
from adventofcode.util.input_helpers import get_input_for_day


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"File({self.name}, {self.size})"


class Directory:

    def __init__(self, parent: Optional["Directory"], name: str):
        self.parent = parent
        self.name = name
        self._files: Dict[str, Union[File, "Directory"]] = {}

    @property
    def files(self) -> Dict[str, Union[File, "Directory"]]:
        return self._files

    @property
    def is_root(self):
        return self.parent is None

    @property
    def size(self):
        return sum(f.size for f in self.files.values())

    def add_file(self, f: Union[File, "Directory"]):
        self._files[f.name] = f

    def __repr__(self):
        return f"Dir({self.name}, size={self.size})"


class FileSystem:

    def __init__(self, root="/", available_space=70_000_000):
        self.root = Directory(None, root)
        self.cwd: Directory = self.root

        self.available_space = available_space

    @property
    def free_space(self):
        """
        The amount of free space currently available
        """
        return self.available_space - self.root.size

    def space_needed_for(self, goal_free_space: int):
        """
        Calculates how much space needs to be freed up in order to the
        desired amount of free_space
        """
        if self.free_space >= goal_free_space:
            return 0
        return goal_free_space - self.free_space

    def change_dir(self, to):
        """
        Changes the directory to the directory with the given name if present
        """
        if to == "..":
            if self.cwd.is_root:
                raise ValueError("Root directory has no parent.")
            self.cwd = self.cwd.parent
        elif to == "/":
            self.cwd = self.root
        else:
            if to not in self.cwd.files:
                raise ValueError(f"Directory {to} does not exist.")
            elif not isinstance(self.cwd.files[to], Directory):
                raise ValueError(f"{to} is not a directory.")
            else:
                self.cwd = self.cwd.files[to]

    def iter_files(self) -> Generator[Union[File, Directory], None, None]:
        """
        Iterates all files in a breadth first manner
        """
        queue = [self.cwd]
        while queue:
            directory = queue.pop()
            for name, f in directory.files.items():
                if isinstance(f, Directory):
                    queue.append(f)
                yield f

    def iter_dirs(self) -> Generator[Directory, None, None]:
        """
        Iterates all directories in a breadth first manner
        """
        for f in self.iter_files():
            if isinstance(f, Directory):
                yield f

    def __repr__(self):
        return str(self.root)


def read_output(lines: List[str], stop: Callable[[str], bool]) -> Tuple[int, List[str]]:
    results = []
    i = 0
    for i, line in enumerate(lines):
        if not stop(line):
            results.append(line)
        else:
            break
    return i, results


def build_fs(results: List[str]):

    fs = FileSystem()
    assert results[0] == "$ cd /"
    line_number = 1

    is_command = lambda l: l.startswith("$")
    while line_number < len(results) - 1:
        output = results[line_number]

        lines_read = 0
        if is_command(output):
            parts = output[2:].split()
            if parts[0] == "cd":
                assert len(parts) == 2
                fs.change_dir(parts[1])
                lines_read = 1
            elif parts[0] == "ls":
                lines_read, files = read_output(results[line_number + 1:], is_command)
                lines_read += 1
                for file in files:
                    properties, name = file.split()
                    if properties == "dir":
                        fs.cwd.add_file(Directory(parent=fs.cwd, name=name))
                    elif properties.isdigit():
                        fs.cwd.add_file(File(name, int(properties)))

            else:
                raise ValueError(f"Unknown command '{parts[0]}'.")

        assert lines_read != 0
        line_number += lines_read

    return fs


def find_free_space(fs: FileSystem, threshold: int):
    if not fs.cwd.is_root:
        fs.change_dir("/")

    possible_free_space = 0
    for directory in fs.iter_dirs():
        if directory.size <= threshold:
            possible_free_space += directory.size

    return possible_free_space


def find_smallest_dir_with_enough_space(fs: FileSystem, space_needed: int):
    smallest = math.inf
    for directory in fs.iter_dirs():
        if directory.size >= space_needed:
            smallest = min(smallest, directory.size)

    return smallest


@solution_timer(2022, 7, 1)
def part_one(fs: FileSystem):
    answer = find_free_space(fs, 100000)

    if not answer:
        raise SolutionNotFoundException(2022, 7, 1)

    return answer


@solution_timer(2022, 7, 2)
def part_two(fs: FileSystem):
    answer = find_smallest_dir_with_enough_space(fs, fs.space_needed_for(30_000_000))

    if not answer:
        raise SolutionNotFoundException(2022, 7, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2022, 7)
    file_system = build_fs(data)
    part_one(file_system)
    part_two(file_system)
