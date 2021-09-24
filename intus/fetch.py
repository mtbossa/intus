"""
Contains functions for fetching the API
and download the medias.
"""
import json
import os

import requests

from intus import config
from intus import generate


def current_display_posts_api() -> bool:
    """
    Check the API of the correspondent display
    for posts updates.
    :return: bool Only for printing in the console
    """
    print('fetching data')
    api_url = config.get_api_url()

    if not os.path.isfile(config.get_etag_json_file_path()):
        etag = '""'
        generate.generate_etag_json(etag)

    with open(config.get_etag_json_file_path(), 'r') as f:
        etag_json = json.loads(f.read())

    last_etag = etag_json['etag']

    headers = {'If-None-Match': last_etag}

    api_response = requests.get(api_url, headers=headers)

    if api_response.status_code == 200:
        print('new data found')

        generate.generate_etag_json(api_response.headers['ETag'])

        content = json.loads(api_response.content)

        generate.generate_local_data_json(content)

        return True

    return False
