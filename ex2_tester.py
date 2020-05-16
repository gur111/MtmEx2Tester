#!/usr/bin/env python3
import hw2
import subprocess
import os
import sys
import select
from io import StringIO
from termcolor import colored

# check if we have more to read from the pipe


def more_data(pipe_out):
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


def check_test_results(part_func, input_file):
    pipe_out, stdout = redirect()

    # Run the test part itself
    part_func(input_file)

    restore_stdout(stdout=stdout)
    # The output we got while redirecting
    return read_pipe(pipe_out=pipe_out).decode()


def print_status(has_failed, part):
    print(f'{test_name} part{part}: '
          f'{colored("passed", "green") if not has_curr_failed else colored("failed", "red")}')


def run_part_a(test_file):
    hw2.partA(test_file)


def run_part_b(test_file):
    # hw2.partA(test_file)
    hw2.partB(test_file)

if __name__ == '__main__':
    test_pairs = []

    in_path = os.path.join('tests', 'in')
    out_path = os.path.join('tests', 'out')

    for test_file_name in os.listdir(in_path):
        out_file_name = test_file_name.replace("test", "out")
        test_pairs.append((os.path.join(in_path, test_file_name),
                           os.path.join(out_path, out_file_name)))

    has_failed = False
    status_format = '{test_name} partA: {colored("passed", "green") if not has_curr_failed else colored("failed", "red")}'

    for test in test_pairs:
        with open(test[1]) as f:
            expected = f.read()

        part_b_index = expected.index('The winner')

        test_name = os.path.splitext(os.path.basename(test[0]))[0]

        # Test partA
        part_expected_results = expected[:part_b_index]
        test_results = check_test_results(part_func=run_part_a,
                                          input_file=test[0])


        has_curr_failed = part_expected_results != test_results
        has_failed = has_failed or has_curr_failed
        print_status(has_failed=has_curr_failed, part='A')

        if has_curr_failed:
            print(f'Got:\n====\tGOT START\n{test_results}\n====\tGOT END')
            print(f'Expected:\n====\tEXPECTED START\n{part_expected_results}\n====\tEXPECTED END')

        
        # Test partB
        part_expected_results = expected[part_b_index:]
        test_results = check_test_results(part_func=run_part_b,
                                          input_file=test[0])

        has_curr_failed = part_expected_results != test_results
        has_failed = has_failed or has_curr_failed
        print_status(has_failed=has_curr_failed, part='B')

        if has_curr_failed:
            print(f'Got:\n{test_results}')
            print(f'Expected:\n{part_expected_results}')
            

    print(("All tests " + colored("passed", "green"))
          if not has_failed else ("Some tests have "+colored("failed", "red")))
