import os
from time import sleep

import generate_index
import fetch
import chrome
import utils

display_id = 3


def main():
    if not (os.path.isfile('local_data.json')):
        chrome.open_file('loader.html')
    else:
        chrome.open_file('index.html')
        total_duration = utils.get_total_duration_seconds('local_data.json')
        sleep(total_duration)

    while True:
        if fetch.fetch_api(display_id):
            generate_index.generate('local_data.json')
            chrome.close()
            chrome.open_file('index.html')
            total_duration = utils.get_total_duration_seconds('local_data.json')
            sleep(total_duration)
        else:
            total_duration = utils.get_total_duration_seconds('local_data.json')
            sleep(total_duration)


main()
