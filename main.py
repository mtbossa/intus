import os
import threading
import time

import generate
import fetch
import chrome
import webserver

DISPLAY_ID = 3
REQUEST_TIME = 10


def main() -> None:
    # Opens the loader if first time opening the Raspberry
    if not (os.path.isfile('local_data.json')):
        chrome.open_file('loader.html')

        # Fetches the API
        fetch.current_display_posts_api(DISPLAY_ID)

        # Generates the index.html after complete fetching
        generate.index('local_data.json')

        # Closes Chrome, which current is showing the loader.html
        chrome.close()

        # Opens Chrome with the newly created index.html
        chrome.open_file('index.html')
    else:
        chrome.open_file('index.html')

    # Keeps checking for API updates, re-generating the local_data.json
    while True:
        if fetch.current_display_posts_api(DISPLAY_ID):
            generate.index('local_data.json')
            time.sleep(REQUEST_TIME)
        else:
            print('no new data found')
            time.sleep(REQUEST_TIME)


# Start the local server to serve the Javascript inside index.html so it can fetch the local_data.json file
threading.Thread(target=webserver.run_server).start()

# Starts the main code
main()
