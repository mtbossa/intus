"""
Functions related to the browser (Chrome).
"""
import os

import utils


def open_file(file_name: str) -> None:
    """
    Issue the command for opening
    the browser with designated file.
    """
    command = utils.get_open_command(file_name)

    os.popen(command)


def close() -> None:
    """Issue the command for closing the browser."""
    command = utils.get_close_command()

    os.system(command)
