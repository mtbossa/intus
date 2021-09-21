""" Generic functions"""
import datetime
import os
import pathlib
import platform
from os import listdir
from os.path import isfile, join


def get_open_command(file_name: str) -> str:
    """
    Return the command for opening either Chrome or Chromium based
    on the OS and file name.
    :param file_name: str Name of the file that chrome will open
    :return: str The complete command for opening chrome with the selected file
    """
    INDEX_FILE_PATH = _get_index_file_path(file_name)

    if platform.system() == 'Windows':
        return 'chrome "' + INDEX_FILE_PATH + '" /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                              '--disable-infobars'

    return 'chromium-browser ' + INDEX_FILE_PATH + ' --incognito --start-fullscreen --disable-crash-reporter'


def _get_index_file_path(file_name: str) -> str:
    """
    Return the index.html file path using pathlib library.
    :param file_name: str Name of the file
    :return: str Correct path to index file
    """
    return str(pathlib.Path(file_name).absolute())


def get_close_command() -> str:
    """
    Return the command for opening either
    Chrome or Chromium based on the OS and file name.
    :return: str Command for killing chrome
    """
    if platform.system() == 'Windows':
        return 'TASKKILL /F /IM chrome.exe'

    return 'killall chromium-browse'


def transform_date_to_epoch(date_string: str) -> float:
    """
    Return the given date string in epoch (int).
    :param date_string: str The date in string format
    :return: float EPOCH time of the given date
    """
    date_time = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    # Transform to int, so won't have decimals, and multiply by 1000 to get milliseconds
    # Needed for javascript Date object creation
    seconds_since_epoch = date_time.timestamp()

    return seconds_since_epoch


def transform_date_to_epoch_seconds(date_string: str) -> float:
    """Return the given date string in epoch (int)"""
    date_time = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    # Transform to int, so won't have decimals, and multiply by 1000 to get milliseconds
    # Needed for javascript Date object creation
    seconds_since_epoch = int(date_time.timestamp() * 1000)

    return seconds_since_epoch


def should_show(start_date: float, end_date: float) -> bool:
    """
    Checks if the post should be shown.
    :param start_date: float Start date of the post in EPOCH float
    :param end_date: End date of the post in EPOCH float
    :return: True if should show, false otherwise
    """
    start_datetime = datetime.datetime.fromtimestamp(start_date)
    end_datetime = datetime.datetime.fromtimestamp(end_date)
    now_datetime = datetime.datetime.now()

    if _check_dates_and_times(start_datetime, end_datetime, now_datetime):
        return True

    return False


def _check_dates_and_times(start_datetime, end_datetime, now_datetime) -> bool:
    """
    Checks date and times of the post, verifying if it should be
    shown of not in the given moment (now).
    :param start_datetime: datetime object Start datetime
    :param end_datetime: datetime object End datetime
    :param now_datetime: datetime object Now datetime
    :return: bool True if should show, false otherwise
    """
    # Verificação 1: a data de início deve ser hoje ou antes de hoje,
    # e a de fim deve ser hoje ou depois de hoje.
    if start_datetime.date() <= now_datetime.date() <= end_datetime.date():
        # Verificações 2: já sei que posso mostrar, pelos dias, mas
        # preciso verificar as horas.

        # Se a hora atual é maior do que a hora de início e menor do que a hora de fim, posso mostrar
        # sem verificar os minutos
        if start_datetime.hour < now_datetime.hour < end_datetime.hour:
            return True

        # Sei que posso mostrar pela hora, pois já passou da hora
        # de início da postagem, não preciso verificar mais as horas
        # e minutos de início, somente de fim
        if start_datetime.hour < now_datetime.hour:
            if end_datetime.hour >= now_datetime.hour and end_datetime.minute > now_datetime.hour.minute:
                # Não preciso verificar os minutos, pois sei que
                # não vai terminar nessa hora ainda.
                return True

        #  Se a hora de início é a mesma da atual, preciso verificar
        #  os minutos de início e fim
        if start_datetime.hour == now_datetime.hour:
            # Só mostro se a o minuto de início for o mesmo ou menor que o minuto atual
            if start_datetime.minute <= now_datetime.minute:
                # Se a hora de fim não a mesma de agora, posso mostrar sem verificar os minutos
                if end_datetime.hour > now_datetime.hour:
                    # Sei que posso mostrar pois não vai terminar nessa hora ainda, então não
                    # preciso verificar os minutos de fim
                    return True
                # Preciso verificar os minutos de fim, pois a hora atual já é a hora de fim
                # Se os minutos de fim forem maiores do que o minuto atual, posso mostrar
                elif end_datetime.minute > now_datetime.minute:
                    return True

    return False

def same_list(l1, l2):
    """
    Checks if a list is the same as the other. Order matters.
    :param l1: list 1
    :param l2: list 2
    :return: bool True if the lists are the same, false otherwise.
    """
    if l1 == l2:
        return True
    else:
        return False


def list_difference(list_1: list, list_2: list) -> list:
    """
    Which values are not in list 1 that are in list 2
    :param list_1: List to find the different values
    :param list_2: List to compare
    :return: List with the values that are in list_1 but no in list_2
    """
    return [item for item in list_1 if item not in list_2]


def delete_file(filename: str) -> None:
    """
    Deletes the given file.
    :param filename: Filename with path
    :return: None
    """
    os.remove(filename)


def get_folder_filenames(folder_path: str) -> list:
    """
    Checks all files inside the given folder.
    :param folder_path: Folder path
    :return: list All files from the folder
    """
    return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]


def create_filename(file_name: str, extension: str) -> str:
    """
    Replaces white spaces of the string with '-' and
    adds a '.' and the extension to the end.
    :param file_name: File name
    :param extension: File extension
    :return: str Transformed filename
    """
    return file_name.replace(' ', '-') + '.' + extension
