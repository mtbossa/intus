"""
Responsible for generating
the index.html page.
"""
import os

import utils

import json

from jinja2 import Environment, FileSystemLoader


def index() -> None:
    """
    Generate index.html page
    using Jinja2 template.
    """
    with open('../data/local_data.json', 'r') as f:
        posts = json.loads(f.read())

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    rendered = env.get_template('display.html').render(posts=posts)

    with open('../resources/index.html', 'w') as f:
        f.write(rendered)


def current_data_for_display(local_data_path) -> bool:
    """
        Checks the current local_data.json to
        regenerate the showcase.json if new
        posts should be checked. showcase.json
        contains only the posts that should be
        passing in the current time.
    """
    with open(local_data_path, 'r') as f:
        local_data_content = json.loads(f.read())

    return _generate_showcase_json(local_data_content)


def _generate_showcase_json(local_data_content: list) -> bool:
    """
    Generate showcase.json, which
    holds the data for which posts should
    be showing in current time. In other words,
    generates de json that has the live posts
    for the javascript to check.
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

    if os.path.isfile('../data/showcase.json'):
        # Compares the current showcase (the stored one) to the new one created
        # Only updates the current showcase if lists are no the same
        # Meaning the showcase was updated here
        if not _compare_new_showcase_to_old(showcase_content):
            local_json_posts = json.dumps(showcase_content, indent=2)

            with open('../data/showcase.json', 'w') as f:
                f.write(local_json_posts)

            return True
    else:
        local_json_posts = json.dumps(showcase_content, indent=2)

        with open('../data/showcase.json', 'w') as f:
            f.write(local_json_posts)

        return True

    return False


def _compare_new_showcase_to_old(new_showcase: list) -> bool:
    # Open the current showcase.json, which hasn't been updated yet
    with open('../data/showcase.json', 'r') as f:
        current_showcase = json.loads(f.read())

    # Compares the lists and return True if they are the same
    # False otherwise
    return utils.same_list(current_showcase, new_showcase)
