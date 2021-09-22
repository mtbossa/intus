import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

import requests

import config
import utils


def download_media(media: dict) -> str:
    """
    Download the media if not already
    downloaded.
    """
    media_url_path = media['path']

    name = media['name']

    extension = media['extension']

    filename = utils.create_filename(name, extension)

    path = os.path.join(config.get_medias_folder(), filename)

    # Only downloads the file if it's not already downloaded
    if not os.path.isfile(path):
        media_url = 'https://intus-medias-paineis.s3.amazonaws.com/' + media_url_path
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
    current_media_filenames = utils.get_folder_filenames(config.get_medias_folder())

    # Filenames that are in list_1 (current local_data) but are not in list_2, new data
    # Meaning these files are not in the local_data and can be deleted
    removed_medias = utils.list_difference(current_media_filenames, new_media_filenames)

    if len(removed_medias) > 0:
        for removed_media_name in removed_medias:
            utils.delete_file(config.get_medias_folder() + removed_media_name)
