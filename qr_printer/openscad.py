#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Some helper utils for qrprinter
"""

import os
import sys


def get_openscad_path():
    """
        Iterate trough common paths to try
        to find openscad
    """
    if sys.platform.startswith('win'):
        return get_openscad_win_path()
    else:
        return get_openscad_lin()


def get_openscad_lin():
    """
        Gets openscad path on linux.
    """
    return "openscad"


def get_openscad_win_path():
    """
        Gets openscad path on windows
    """
    window_paths = [
        os.environ["ProgramFiles"],
        os.environ["ProgramFiles(x86)"],
        os.environ["ProgramW6432"]
    ]

    for path in window_paths:
        openscad_binary = os.path.join(
            path,
            "OpenScad",
            "openscad.exe"
        )
        if os.path.isfile(openscad_binary):
            break

    if not os.path.isfile(openscad_binary):
        raise Exception("could not find openscad in your system")

    return openscad_binary
