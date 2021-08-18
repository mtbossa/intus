import os
import pathlib


def open():
    curret_script_path = str(pathlib.Path(__file__).parent.resolve())

    complete_index_path = '"' + curret_script_path + '\\index.html' + '"'

    print(complete_index_path)

    command = 'chrome ' + complete_index_path + ' --start-fullscreen'

    os.popen(command)

def close():
    os.system("TASKKILL /F /IM chrome.exe")

