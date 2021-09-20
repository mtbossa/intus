"""
The main workflow of the
program, and logic.
"""

import os
import threading
import time

import config
import generate
import fetch
import chrome
import webserver

DISPLAY_ID = config.get_display_id()
REQUEST_TIME = config.get_request_time()


def main() -> None:
    """Runs the main logic of the program."""
    # Opens loader.html if first time opening the Raspberry
    if not os.path.isfile(config.get_local_data_json_file_path()):
        chrome.open_file(config.get_resources_folder() + 'loader.html')

        # Fetches the API
        fetch.current_display_posts_api(DISPLAY_ID)

        # Generates the json for the showcase. Has only the needed posts for the Javascript
        generate.current_data_for_display(config.get_local_data_json_file_path())

        # Generates the index.html after complete fetching
        generate.index()

        # Closes Chrome, which current is showing the loader.html
        chrome.close()

        # Opens Chrome with the newly created index.html
        chrome.open_file(config.get_resources_folder() + 'index.html')

        # Wait the REQUEST_TIME to request updates
        time.sleep(REQUEST_TIME)
    else:
        chrome.open_file(config.get_resources_folder() + 'index.html')

    # Keeps checking for API updates, re-generating the local_data.json and showcase.json
    while True:
        if fetch.current_display_posts_api(DISPLAY_ID):
            print('new data found!')
        else:
            print('no updates')

        if generate.current_data_for_display(config.get_local_data_json_file_path()):
            print('showcase updated')
        else:
            print('showcase not updated')

        time.sleep(REQUEST_TIME)


if __name__ == '__main__':
    # Start the local server index.html can fetch the local_data.json file
    threading.Thread(target=webserver.run_server).start()

    # Starts the main code
    main()
