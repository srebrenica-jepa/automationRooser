#!/usr/bin/env python
import os


def create_folder(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError:
        if not os.path.isdir(folder):
            raise

    return folder
