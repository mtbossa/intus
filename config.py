"""
Functions related to the
config file.
"""

import json


def _get_config_json() -> dict:
    """
    Loads the config.json file and
    returns its content as Python Object.
    """
    with open('.config.json', 'r') as f:
        return json.loads(f.read())


def get_api_url() -> str:
    """
    Return the api_url from the
    config.json file.
    """
    config_json = _get_config_json()

    return config_json['api_url']


def get_display_id() -> int:
    """
    Return the display_id from the
    config.json file.
    """
    config_json = _get_config_json()

    return config_json['display_id']


def get_request_time() -> int:
    """
    Return the request_time from the
    config.json file.
    """
    config_json = _get_config_json()

    return config_json['request_time']
