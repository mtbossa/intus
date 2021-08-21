"""
Generic functions
"""

import pathlib
import platform


def get_command(file_name: str) -> str:
    """
    Return the command based
    on the OS and file name
    """
    INDEX_FILE_PATH = _get_index_file_path(file_name)

    if platform.system() == 'Windows':
        return 'chrome "' + INDEX_FILE_PATH + '" /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                             '--disable-infobars'

    return 'chromium-browser ' + INDEX_FILE_PATH + ' --incognito --start-fullscreen --disable-crash-reporter'


def _get_index_file_path(file_name: str) -> str:
    """
    Return the index.html file
    path
    """
    return str(pathlib.Path(file_name).absolute())
