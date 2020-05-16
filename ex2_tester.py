#!/usr/bin/env python3
import hw2
import hw2comp
import random
import subprocess
import os
import sys
import select
from io import StringIO
from termcolor import colored
from time import sleep
from generate_test_file import generate_test_file


def get_scrambled(file_name):
    import random
    with open(file_name, 'r') as source:
        data = [(random.random(), line) for line in source]
    data.sort()

    # split_file_name = os.path.splitext(file_name)
    scrambled_file_name = 'temp_scrambled.txt'
    with open(scrambled_file_name, 'w') as target:
        for _, line in data:
            target.write(line)

    return scrambled_file_name


def more_data(pipe_out):
    """ check if we have more to read from the pipe """
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)

# read the whole pipe


def read_pipe(pipe_out):
    out = b''
    while more_data(pipe_out):
        out += os.read(pipe_out, 1024)

    return out


def redirect():
    sys.stdout.write(' \b')
    pipe_out, pipe_in = os.pipe()
    # save a copy of stdout
    stdout = os.dup(1)
    # replace stdout with our write pipe
    os.dup2(pipe_in, 1)

    return pipe_out, stdout


def restore_stdout(stdout):
    os.dup2(stdout, 1)


def check_test_results(input_file):
    pipe_out, stdout = redirect()

    # Run the test part itself
    scambled_file = get_scrambled(input_file)
    run_part_a(scambled_file)
    run_part_b(scambled_file)

    restore_stdout(stdout=stdout)
    # The output we got while redirecting
    return read_pipe(pipe_out=pipe_out).decode()


def print_status(has_failed):
    print(f'{test_name}: '
          f'{colored("passed", "green") if not has_curr_failed else colored("failed", "red")}')


def run_part_a(test_file):
    hw2.partA(test_file)


def run_part_b(test_file):
    # hw2.partA(test_file)
    hw2.partB(test_file)


if __name__ == '__main__':
    in_file = 'temp_test.txt'
    out_file = 'temp_test.out'
    # generate_test_file(test_file_path=in_file, out_file_path=out_file)
    # test_pairs = []

    # in_path = os.path.join('tests', 'in')
    # out_path = os.path.join('tests', 'out')

    # for test_file_name in os.listdir(in_path):
    #     if not test_file_name.startswith("test"):
    #         continue

    #     out_file_name = test_file_name.replace("test", "out")
    #     test_pairs.append((os.path.join(in_path, test_file_name),
    #                        os.path.join(out_path, out_file_name)))

    has_failed = False
    # status_format = '{test_name} partA: {colored("passed", "green") if not has_curr_failed else colored("failed", "red")}'

    for _ in range(100):
        sleep(0.1)
        test = (in_file, out_file)
        generate_test_file(test_file_path=in_file, out_file_path=out_file)
    # for test in test_pairs:
        with open(test[1]) as f:
            expected = f.read()

        # part_b_index = part_b_index if part_b_index != -1 else 

        test_name = os.path.splitext(os.path.basename(test[0]))[0]

        # Run Test
        expected_results = expected
        test_results = check_test_results(input_file=test[0])

        has_curr_failed = expected_results != test_results
        has_failed = has_failed or has_curr_failed
        print_status(has_failed=has_curr_failed)

        if has_curr_failed:
            print(f'Got:\n====\tGOT START\n{test_results}\n====\tGOT END')
            print(
                f'Expected:\n====\tEXPECTED START\n{expected_results}\n====\tEXPECTED END')
            exit(1)

    print(("All tests " + colored("passed", "green"))
          if not has_failed else ("Some tests have "+colored("failed", "red")))
