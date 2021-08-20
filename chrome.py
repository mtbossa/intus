import time
from datetime import datetime
import os
import pathlib


def open_file(file_name: str) -> None:
    current_script_path = str(pathlib.Path(__file__).parent.resolve())

    complete_index_path = '"' + current_script_path + '\\' + file_name + '"'

    command = 'chrome ' + complete_index_path + ' /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                                '--disable-infobars'

    os.popen(command)


def close() -> None:
    os.system("TASKKILL /F /IM chrome.exe")

