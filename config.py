import json

def get_config_json() -> dict:
    with open('config.json', 'r') as f:
        return json.loads(f.read())

def get_api_url() -> str:
    config_json = get_config_json()

    return config_json['api_url']

def get_display_id() -> int:
    config_json = get_config_json()

    return config_json['display_id']


def get_request_time() -> int:
    config_json = get_config_json()

    return config_json['request_time']
