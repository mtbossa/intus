import os
import threading
import time

import generate_index
import fetch
import chrome
import webserver

display_id = 3
request_time = 60


def main():
    # Opens the loader if first time opening the Raspberry
    if not (os.path.isfile('local_data.json')):
        chrome.open_file('loader.html')
        fetch.fetch_api(display_id)
        generate_index.generate('local_data.json')
        chrome.close()
        chrome.open_file('index.html')
    else:
        chrome.open_file('index.html')

    while True:
        if fetch.fetch_api(display_id):
            generate_index.generate('local_data.json')
            time.sleep(request_time)
        else:
            print('no new data found')
            time.sleep(request_time)


# Start the local server so the Javascript inside index.html can fetch the local_data.json file
threading.Thread(target=webserver.run_server).start()

# Starts the main code
main()
