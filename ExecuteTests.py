#!/usr/bin/env python
import os

from TestExecute.RunManager import RunManager

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_runner = RunManager()
    test_runner.run_selection()
