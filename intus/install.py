"""
Install needed files.
"""
import os
import shutil

import pkg_resources

from intus import config, generate, chrome, fetch


def install() -> None:
    os.makedirs(config.get_config_folder(), exist_ok=True)
    os.makedirs(config.get_data_folder(), exist_ok=True)
    os.makedirs(config.get_medias_folder(), exist_ok=True)

    try:
        resources_location = pkg_resources.resource_filename('intus', 'resources')
        shutil.copytree(resources_location, config.get_resources_folder())
    finally:
        pkg_resources.cleanup_resources()

    while True:
        try:
            display_id = int(input("ID do display: "))
        except ValueError:
            print('Insira um número.')
            # better try again... Return to the start of the loop
            continue

        if display_id < 0:
            print('Insira um número maior do que 0.')
            continue
        else:
            # Successfully parsed!
            # we're ready to exit the loop.
            generate.config_file(display_id)
            break

    # Opens loader.html if first time opening the Raspberry
    chrome.open_file(config.get_loader_file_path())

    # Fetches the API
    fetch.current_display_posts_api()

    # Generates the json for the showcase. Has only the needed posts for the Javascript
    generate.current_data_for_display(config.get_local_data_json_file_path())

    # Generates the index.html after complete fetching
    generate.index()

    # Closes Chrome, which current is showing the loader.html
    chrome.close()
