#!/usr/bin/env python3
import hw2
import os
import sys
from io import StringIO
from termcolor import colored

if __name__ == '__main__':
    test_pairs = []

    in_path = os.path.join('tests', 'in')
    out_path = os.path.join('tests', 'out')

    for test_file_name in os.listdir(in_path):
        out_file_name = test_file_name.replace("test", "out")
        test_pairs.append((os.path.join(in_path, test_file_name),
                           os.path.join(out_path, out_file_name)))

    has_failed = False

    for test in test_pairs:
        stdout_stream = StringIO()
        with open(test[1]) as f:
            expected = f.read()

        stdout, sys.stdout = sys.stdout, stdout_stream

        hw2.partA(test[0])
        sys.stdout = stdout
        stdout_stream.seek(0)
        actual = stdout_stream.read()

        has_curr_failed = actual == expected[:len(actual)]
        has_failed = has_failed and has_curr_failed
        test_name = os.path.splitext(os.path.basename(test[0]))[0]
        print(f'{test_name}: '
              f'{colored("passed", "green") if has_curr_failed else colored("failed", "red")}')

    print(("All tests " + colored("passed", "green"))
          if not has_failed else ("Some tests have "+colored("failed", "red")))
