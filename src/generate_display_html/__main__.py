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


def main() -> None:
    """Runs the main logic of the program."""

    # Initial configuration
    if not os.path.isfile(os.path.join(config.get_config_folder(), '.config.json')):

        os.makedirs(config.get_config_folder(), exist_ok=True)
        os.makedirs(config.get_data_folder(), exist_ok=True)
        os.makedirs(config.get_resources_folder(), exist_ok=True)
        os.makedirs(config.get_medias_folder(), exist_ok=True)

        while True:
            try:
                display_id = int(input("ID do display: "))
            except ValueError:
                print('Insira um número.')
                # better try again... Return to the start of the loop
                continue

            if display_id < 0:
                print('Insira um número maior do que 0.')
                continue
            else:
                # Successfully parsed!
                # we're ready to exit the loop.
                generate.config_file(display_id)
                break

    # Start the local server index.html can fetch the local_data.json file
    threading.Thread(target=webserver.run_server).start()

    # Opens loader.html if first time opening the Raspberry
    if not os.path.isfile(config.get_local_data_json_file_path()):
        chrome.open_file(os.path.abspath('../resources/loader.html'))

        # Fetches the API
        fetch.current_display_posts_api()

        # Generates the json for the showcase. Has only the needed posts for the Javascript
        generate.current_data_for_display(config.get_local_data_json_file_path())

        # Generates the index.html after complete fetching
        generate.index()

        # Closes Chrome, which current is showing the loader.html
        chrome.close()

        # Opens Chrome with the newly created index.html
        chrome.open_file(os.path.join(config.get_resources_folder(), 'index.html'))

        # Wait the REQUEST_TIME to request updates
        time.sleep(config.get_request_time())
    else:
        chrome.open_file(os.path.join(config.get_resources_folder(), 'index.html'))

    # Keeps checking for API updates, re-generating the local_data.json and showcase.json
    while True:
        if fetch.current_display_posts_api():
            print('new data found!')
        else:
            print('no updates')

        if generate.current_data_for_display(config.get_local_data_json_file_path()):
            print('showcase updated')
        else:
            print('showcase not updated')

        time.sleep(config.get_request_time())


if __name__ == '__main__':
    # Starts the main code
    main()
