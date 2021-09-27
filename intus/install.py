"""
Install needed files.
"""
import os
import shutil

import pkg_resources

from intus import config, generate, chrome, fetch


def reinstall() -> None:
    try:
        shutil.rmtree(config.get_app_folder())
        os.rmdir(config.get_intus_folder())
        os.remove(os.path.join(config.get_autostart_folder(), 'autostart-display.desktop'))
        print('Excluindo todos os arquivos...')
        print('Para instalar novamente, execute: python -m intus')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        print('Arquivos já deletados.')


def install() -> None:
    os.makedirs(config.get_config_folder(), exist_ok=True)
    os.makedirs(config.get_data_folder(), exist_ok=True)
    os.makedirs(config.get_medias_folder(), exist_ok=True)
    # Create the autostart dir inside .config folder
    os.makedirs(config.get_autostart_folder(), exist_ok=True)

    try:
        resources_location = pkg_resources.resource_filename('intus', 'resources')
        shutil.copytree(resources_location, config.get_resources_folder())

        shutil.move(os.path.join(config.get_installation_folder(), 'autostart-display.desktop'),
                    os.path.join(config.get_autostart_folder(), 'autostart-display.desktop'))
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
