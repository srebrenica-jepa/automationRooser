#!/usr/bin/env python
import os

from Common.TestExecute.TestRunner import TestRunner

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_runner = TestRunner()
    test_runner.execute_tests_on_demand()
