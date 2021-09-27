"""
The main workflow of the
program, and logic.
"""

import os
import argparse
import threading
import time

from intus import install, generate, config, fetch, chrome, webserver


def main() -> None:
    """Runs the main logic of the program."""

    parser = argparse.ArgumentParser(description='Reinstalar programa.')

    parser.add_argument('-r', '--reinstalar', action='store_true', help='Excluir todos os dados.')

    args = parser.parse_args()

    if args.reinstalar:
        install.reinstall()
        exit()

    # Initial configuration
    if not os.path.isfile(os.path.join(config.get_config_folder(), '.config.json')):
        install.install()

        # Opens loader.html if first time opening the Raspberry
        chrome.open_file(config.get_loader_file_path())

        # Fetches the API
        fetch.current_display_posts_api()

        # Generates the json for the showcase. Has only the needed posts for the Javascript
        generate.current_data_for_display(config.get_local_data_json_file_path())

        # Generates the index.html after complete fetching
        generate.index()

        # Closes Chrome, which current is showing the loader.html
        chrome.close()

    # Start the local server
    # index.html can fetch the showcase.json file
    threading.Thread(target=webserver.run_server, daemon=True).start()

    chrome.open_file(config.get_index_file_path())

    # Keeps checking for API updates, re-generating the local_data.json and showcase.json
    while True:
        try:
            if fetch.current_display_posts_api():
                print('new data found!')
            else:
                print('no updates')

            if generate.current_data_for_display(config.get_local_data_json_file_path()):
                print('showcase updated')
            else:
                print('showcase not updated')

            time.sleep(config.get_request_time())

        except KeyboardInterrupt:
            print('exiting')
            exit()


if __name__ == '__main__':
    # Starts the main code
    main()

