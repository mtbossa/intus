import asyncio
import os
import time
from datetime import datetime

import generate_index
import fetch
import chrome
import utils

display_id = 3


async def main():
    start_time = 0
    if not (os.path.isfile('local_data.json')):
        chrome.open_file('loader.html')
    else:
        chrome.open_file('index.html')
        start_time = datetime.now()

    while True:
        if fetch.fetch_api(display_id):
            current_total_duration = utils.get_total_duration('local_data.json')
            generate_index.generate('local_data.json')
            if start_time != 0:
                await chrome.finish_posts(start_time, current_total_duration)
            chrome.close()
            chrome.open_file('index.html')
            start_time = datetime.now()
            time.sleep(10)
        else:
            print('no new data found')
            time.sleep(10)


asyncio.run(main())
