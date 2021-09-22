"""
Functions related to the
config file.
"""

import json
import os.path
from pathlib import Path

APP_NAME = 'GenerateDisplayHtml'
APP_AUTHOR = 'Intus'
APP_FOLDER = os.path.join(Path.home(), APP_AUTHOR, APP_NAME)


def _get_config_data() -> dict:
    """
    Loads the config.json file and
    returns its content as Python Object.
    """
    with open(os.path.join(get_config_folder(), '.config.json'), 'r') as f:
        return json.loads(f.read())


def get_api_url() -> str:
    """
    Return the api_url from the
    config.json file.
    """
    config_json = _get_config_data()

    return config_json['api_url']


def get_display_id() -> int:
    """
    Return the display_id from the
    config.json file.
    """
    config_json = _get_config_data()

    return config_json['display_id']


def get_request_time() -> int:
    """
    Return the request_time from the
    config.json file.
    """
    config_json = _get_config_data()

    return config_json['request_time']


def get_config_folder() -> str:
    return os.path.join(APP_FOLDER, 'config')


def get_resources_folder() -> str:
    return os.path.join(APP_FOLDER, 'resources')


def get_medias_folder() -> str:
    return os.path.join(APP_FOLDER, 'medias')


def get_data_folder() -> str:
    return os.path.join(APP_FOLDER, 'data')


def get_local_data_json_file_path() -> str:
    return os.path.join(get_data_folder(), 'local_data.json')


def get_showcase_json_file_path() -> str:
    return os.path.join(get_data_folder(), 'showcase.json')


def get_etag_json_file_path() -> str:
    return os.path.join(get_data_folder(), 'etag.json')
