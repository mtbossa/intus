"""
Responsible for generating
the index.html page.
"""
import os

import utils

import json

from jinja2 import Environment, FileSystemLoader

import medias
import config


def index() -> None:
    """
    Generate index.html page
    using Jinja2 template.
    :return: None
    """
    with open(config.get_local_data_json_file_path(), 'r') as f:
        posts = json.loads(f.read())

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    rendered = env.get_template('display.html').render(posts=posts)

    with open(config.get_resources_folder() + '/index.html', 'w') as f:
        f.write(rendered)


def current_data_for_display(local_data_path) -> bool:
    """
    Checks the current local_data.json to
    regenerate the showcase.json if new
    posts should be checked. showcase.json
    contains only the posts that should be
    passing in the current time.
    :param local_data_path: str Path to the current local_data.json
    :return: bool Only for printing in the console
    """
    with open(local_data_path, 'r') as f:
        local_data_content = json.loads(f.read())

    return _generate_showcase_json(local_data_content)


def _generate_showcase_json(local_data_content: list) -> bool:
    """
    Generate showcase.json, which
    holds the data for which posts should
    be showing in current time. In other words,
    generates the JSON that has the live posts
    for the Javascript to check.
    :param local_data_content: list Contents from the current local_data.json
    :return: bool Only for printing in the console
    """
    showcase_content = []
    for post_data in local_data_content:
        # Verificar a data (lógica javascript) e dar append ou não no post
        if utils.should_show(post_data['start_date'], post_data['end_date']):
            showcase_content.append({
                'post_id': post_data['post_id'],
                'media_name': post_data['media_name'],
                'media_duration': post_data['media_duration'],
                'media_type': post_data['media_type'],
                'media_extension': post_data['media_extension'],
                'local_path': post_data['local_path']
            })

    if os.path.isfile(config.get_showcase_json_file_path()):
        # Compares the current showcase (the stored one) to the new one created
        # Only updates the current showcase if lists are no the same
        # Meaning the showcase was updated here
        if not _compare_new_showcase_to_old(showcase_content):
            local_json_posts = json.dumps(showcase_content, indent=2)

            with open(config.get_showcase_json_file_path(), 'w') as f:
                f.write(local_json_posts)

            return True
    else:
        local_json_posts = json.dumps(showcase_content, indent=2)

        with open(config.get_showcase_json_file_path(), 'w') as f:
            f.write(local_json_posts)

        return True

    return False


def _compare_new_showcase_to_old(new_showcase: list) -> bool:
    """
    Compares the new showcase content from the old one
    so it don't get updated every time, only when
    they are different
    :param new_showcase: list Contents from the new showcase data
    :return: bool True if old and new showcase are the same
    """
    # Open the current showcase.json, which hasn't been updated yet
    with open(config.get_showcase_json_file_path(), 'r') as f:
        current_showcase = json.loads(f.read())

    # Compares the lists and return True if they are the same
    # False otherwise
    return utils.same_list(current_showcase, new_showcase)


def generate_etag_json(etag: str) -> None:
    """
    Generate etag.json file which
    holds the last response ETag.
    :param etag: str ETag from the API response
    :return: None
    """
    etag_dict = {
        'etag': etag
    }
    json_string = json.dumps(etag_dict)

    with open(config.get_etag_json_file_path(), 'w') as f:
        f.write(json_string)


def generate_local_data_json(content: dict) -> None:
    """
    Generate local_data.json which
    holds the local data info for Javascript usage.
    Also checks if any media should be deleted.
    :param content: dict Data from the API already converted from JSON
    :return: None
    """
    posts_list = []
    new_media_names_list = []

    for post in content['posts']:
        # The name is needed for later verifying if any media should be deleted
        new_media_names_list.append(utils.create_filename(post['media']['name'], post['media']['extension']))

        complete_path = medias.download_media(post['media'])

        posts_list.append({
            'post_id': post['id'],
            'media_name': post['media']['name'],
            'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/' + post['media']['path'],
            'media_duration': post['duration'],
            'media_type': post['media']['type'],
            'media_extension': post['media']['extension'],
            'start_date': utils.transform_date_to_epoch(post['start_date']),
            'end_date': utils.transform_date_to_epoch(post['end_date']),
            'local_path': complete_path
        })

    # Will check if any media should be deleted
    medias.check_deletion(new_media_names_list)

    local_json_posts = json.dumps(posts_list, indent=2)

    with open(config.get_local_data_json_file_path(), 'w') as f:
        f.write(local_json_posts)
