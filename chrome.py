import time
from datetime import datetime
import os
import pathlib


def open_file(file_name):
    current_script_path = str(pathlib.Path(__file__).parent.resolve())

    complete_index_path = '"' + current_script_path + '\\' + file_name + '"'

    command = 'chrome ' + complete_index_path + ' /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                                '--disable-infobars'

    os.popen(command)


def close():
    os.system("TASKKILL /F /IM chrome.exe")


async def finish_posts(start_time, current_total_duration):
    now_time = datetime.now()
    print('waiting for post to fnisih')
    while True:
        elapsed = now_time - start_time
        # Get the interval in milliseconds
        diff_in_milli_secs = int(elapsed.total_seconds() * 1000)
        if diff_in_milli_secs % current_total_duration == 0:
            print('ended')
            return True
        else:
            now_time = datetime.now()
