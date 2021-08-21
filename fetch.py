import os

import requests
import json

import config


def current_display_posts_api(display_id: int) -> bool:
    print('fetching data')
    api_url = config.get_api_url() + str(display_id)

    if not (os.path.isfile('etag.json')):
        etag = '""'
        generate_etag_json(etag)

    with open('etag.json', 'r') as f:
        etag_json = json.loads(f.read())

    last_etag = etag_json['etag']

    headers = {'If-None-Match': last_etag}

    api_response = requests.get(api_url, headers=headers)

    if api_response.status_code == 200:
        print('new data found')

        generate_etag_json(api_response.headers['ETag'])

        content = json.loads(api_response.content)

        generate_local_json(content)

        return True
    else:
        return False


def generate_etag_json(etag: str) -> None:
    etag_dict = {
        'etag': etag
    }
    json_string = json.dumps(etag_dict)

    with open('etag.json', 'w') as f:
        f.write(json_string)


def generate_local_json(content: dict) -> None:
    posts_dict = []
    for post in content['posts']:
        complete_path = download_media(post['media'])
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

    with open('local_data.json', 'w') as f:
        f.write(local_json_posts)


def download_media(media: dict) -> str:
    if not (os.path.isdir('medias')):
        os.mkdir('medias')

    path = media['path']

    name = media['name']

    extension = media['extension']

    file_name = name.replace(' ', '-') + '.' + extension

    complete_path = 'medias/' + file_name

    # Only downloads the file if it's not already downloaded
    if not (os.path.isfile(complete_path)):
        media_url = 'https://intus-medias-paineis.s3.amazonaws.com/' + path
        print('downloading media')
        media_response = requests.get(media_url)

        with open(complete_path, 'wb') as f:
            f.write(media_response.content)

    return complete_path
