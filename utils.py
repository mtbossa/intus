import json


def get_total_duration_seconds(local_data):
    with open(local_data, 'r') as f:
        posts = json.loads(f.read())

    total_duration = 0

    for post in posts:
        total_duration += post['media_duration']

    return total_duration / 1000
