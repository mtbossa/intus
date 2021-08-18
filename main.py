import time
import asyncio

import generate_index
import fetch
import chrome
import utils

display_id = 3

while True:
    fetch.fetch_api(display_id)

    total_duration = utils.get_total_duration('local_data.json')

    generate_index.generate('local_data.json')

    chrome.open()

    time.sleep(5)
