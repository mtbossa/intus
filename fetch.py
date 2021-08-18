import os

import requests
import json


def fetch_api(display_id):
    api_url = 'http://localhost/api/fetch-display-posts/' + str(display_id)

    if not (os.path.isfile('etag.json')):
        etag = '""'
        generate_etag_json(etag)

    with open('etag.json', 'r') as f:
        etag_json = json.loads(f.read())

    last_etag = etag_json['etag']

    headers = {'If-None-Match': last_etag}

    api_response = requests.get(api_url, headers=headers)

    print(api_response.status_code)

    if api_response.status_code == 200:

        generate_etag_json(api_response.headers['ETag'])

        content = json.loads(api_response.content)

        if not (os.path.isfile('local_data.json')):
            generate_local_json(content)
        else:
            generate_local_json(content)


def generate_etag_json(etag):
    etag_dict = {
        'etag': etag
    }
    json_string = json.dumps(etag_dict)

    with open('etag.json', 'w') as f:
        f.write(json_string)


def generate_local_json(content):
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


def download_media(media):
    if not (os.path.isdir('medias')):
        os.mkdir('medias')

    path = media['path']

    name = media['name']

    extension = media['extension']

    file_name = name.replace(' ', '-') + '.' + extension

    complete_path = 'medias/' + file_name

    if not (os.path.isfile(complete_path)):
        media_url = 'https://intus-medias-paineis.s3.amazonaws.com/' + path

        media_response = requests.get(media_url)

        with open(complete_path, 'wb') as f:
            f.write(media_response.content)

    return complete_path


