"""
Contains functions for fetching the API
and download the medias.
"""

import os

import json
from pathlib import Path

import requests

import config


def current_display_posts_api(display_id: int) -> bool:
    """
    Check the API of the correspondent display
    for posts updates.
    """
    print('fetching data')
    api_url = config.get_api_url() + str(display_id)

    if not os.path.isfile('../data/etag.json'):
        etag = '""'
        _generate_etag_json(etag)

    with open('../data/etag.json', 'r') as f:
        etag_json = json.loads(f.read())

    last_etag = etag_json['etag']

    headers = {'If-None-Match': last_etag}

    api_response = requests.get(api_url, headers=headers)

    if api_response.status_code == 200:
        print('new data found')

        _generate_etag_json(api_response.headers['ETag'])

        content = json.loads(api_response.content)

        _generate_local_json(content)

        return True

    return False


def _generate_etag_json(etag: str) -> None:
    """
    Generate etag.json file which
    holds the last response ETag.
    """
    etag_dict = {
        'etag': etag
    }
    json_string = json.dumps(etag_dict)

    with open('../data/etag.json', 'w') as f:
        f.write(json_string)


def _generate_local_json(content: dict) -> None:
    """
    Generate local_data.json which
    holds the local data info for Javascript usage.
    """
    posts_dict = []
    for post in content['posts']:
        complete_path = _download_media(post['media'])
        posts_dict.append({
            'post_id': post['id'],
            'media_name': post['media']['name'],
            'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/' + post['media']['path'],
            'media_duration': post['duration'],
            'media_type': post['media']['type'],
            'media_extension': post['media']['extension'],
            'local_path': complete_path
        })

    local_json_posts = json.dumps(posts_dict, indent=2)

    with open('../data/local_data.json', 'w') as f:
        f.write(local_json_posts)


def _download_media(media: dict) -> str:
    """
    Download the media if not already
    downloaded.
    """
    if not os.path.isdir('../resources/medias'):
        os.mkdir('../resources/medias')

    media_url_path = media['path']

    name = media['name']

    extension = media['extension']

    file_name = name.replace(' ', '-') + '.' + extension

    path = '../resources/medias/' + file_name

    # Only downloads the file if it's not already downloaded
    if not os.path.isfile(path):
        media_url = 'https://intus-medias-paineis.s3.amazonaws.com/' + media_url_path
        print('downloading media: ' + file_name)
        media_response = requests.get(media_url)

        with open(path, 'wb') as f:
            f.write(media_response.content)
            complete_path = str(Path(f.name))

            print(complete_path)

    else:
        complete_path = str(Path(path))
        print(complete_path)

    return complete_path

