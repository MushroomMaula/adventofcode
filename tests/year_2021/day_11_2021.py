from copy import deepcopy

from adventofcode.year_2021.day_11_2021 import parse_inputs, Swarm, flatten


def _log_message(a, b):
    msg = ''
    for line_a, line_b in zip(a, b):
        msg += ''.join(map(str, line_a)) + '\t' + ''.join(map(str, line_b)) + '\n'

    return msg


def parse_test_inputs():
    inputs = []
    with open("day_11_test_inputs.txt", 'r') as f:
        step = []
        for line in f:
            if line.strip() == '':
                inputs.append(parse_inputs(step))
                step = []
            else:
                step.append(line.strip())
    inputs.append(parse_inputs(step))
    return inputs


def test_steps():
    octopi, *test_inputs = parse_test_inputs()
    for i, result in enumerate(test_inputs, start=1):
        values = deepcopy(octopi)
        s = Swarm(values)
        for _ in range(i):
            s.simulate()

        try:
            assert list(flatten(values)) == list(flatten(result)), f"Step {i=} does not match"
        except AssertionError as e:
            print(f"\nFailed at step: {i}\n{_log_message(values, result)}")
            raise e
