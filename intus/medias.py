"""
Medias handling functions.
"""

import os
from pathlib import Path

import requests

from intus import config
from intus import utils


def download_media(media_url: str, media_name: str, media_extension: str) -> str:
    """
    Download the media if not already
    downloaded.
    :param media_url: str Download url of the media
    :param media_name: str Media name
    :param media_extension: str Media extension
    """
    name = media_name

    extension = media_extension

    filename = utils.create_filename(name, extension)

    path = os.path.join(config.get_medias_folder(), filename)

    # Only downloads the file if it's not already downloaded
    if not os.path.isfile(path):
        print('downloading media: ' + filename)
        media_response = requests.get(media_url)

        with open(path, 'wb') as f:
            f.write(media_response.content)
            complete_path = str(Path(f.name))

            print(complete_path)
    else:
        complete_path = str(Path(path))
        print(complete_path)

    return complete_path


def check_deletion(new_media_filenames: list) -> None:
    """
    Deletes all medias that aren't needed anymore by comparing
    the needed filenames to the ones already in the medias folder.
    :param new_media_filenames: list containing all the medias filename from the API response
    """
    current_media_filenames = utils.get_folder_filenames(config.get_medias_folder())

    # Filenames that are in list_1 (current local_data) but are not in list_2, new data
    # Meaning these files are not in the local_data and can be deleted
    removed_medias = utils.list_difference(current_media_filenames, new_media_filenames)

    if len(removed_medias) > 0:
        for removed_media_name in removed_medias:
            utils.delete_file(os.path.join(config.get_medias_folder(), removed_media_name))
