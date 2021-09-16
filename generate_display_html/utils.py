""" Generic functions"""
import datetime
import pathlib
import platform


def get_open_command(file_name: str) -> str:
    """
    Return the command for opening either Chrome or Chromium based
    on the OS and file name.
    """
    INDEX_FILE_PATH = _get_index_file_path(file_name)

    if platform.system() == 'Windows':
        return 'chrome "' + INDEX_FILE_PATH + '" /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                              '--disable-infobars'

    return 'chromium-browser ' + INDEX_FILE_PATH + ' --incognito --start-fullscreen --disable-crash-reporter'


def _get_index_file_path(file_name: str) -> str:
    """Return the index.html file path."""
    return str(pathlib.Path(file_name).absolute())


def get_close_command() -> str:
    """
    Return the command for opening either
    Chrome or Chromium based on the OS and file name.
    """
    if platform.system() == 'Windows':
        return 'TASKKILL /F /IM chrome.exe'

    return 'killall chromium-browse'


def transform_date_to_epoch(date_string: str) -> int:
    """Return the given date string in epoch seconds (int)"""
    date_time = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    seconds_since_epoch = int(date_time.timestamp())

    return seconds_since_epoch
