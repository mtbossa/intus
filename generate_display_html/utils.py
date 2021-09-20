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
    """
    INDEX_FILE_PATH = _get_index_file_path(file_name)

    if platform.system() == 'Windows':
        return 'chrome "' + INDEX_FILE_PATH + '" /incognito --start-fullscreen --disable-session-crashed-bubble ' \
                                              '--disable-infobars'

    return 'chromium-browser ' + INDEX_FILE_PATH + ' --incognito --start-fullscreen --disable-crash-reporter'


def _get_index_file_path(file_name: str) -> str:
    """Return the index.html file path."""
    return str(pathlib.Path(file_name).absolute())


def get_close_command() -> str:
    """
    Return the command for opening either
    Chrome or Chromium based on the OS and file name.
    """
    if platform.system() == 'Windows':
        return 'TASKKILL /F /IM chrome.exe'

    return 'killall chromium-browse'


def transform_date_to_epoch(date_string: str) -> float:
    """Return the given date string in epoch (int)"""
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


def should_show(start_date, end_date) -> int:
    start_datetime = datetime.datetime.fromtimestamp(start_date)
    end_datetime = datetime.datetime.fromtimestamp(end_date)
    now_datetime = datetime.datetime.now()

    date_and_times = _getDateAndTimes(start_datetime, end_datetime, now_datetime)

    if _check_dates_and_times(date_and_times):
        return True

    return False


def _check_dates_and_times(date_and_times) -> bool:
    # Verificação 1: a data de início deve ser hoje ou antes de hoje,
    # e a de fim deve ser hoje ou depois de hoje.
    if date_and_times['start']['date_sum'] <= date_and_times['now']['date_sum'] <= date_and_times['end']['date_sum']:
        # Verificações 2: já sei que posso mostrar, pelos dias, mas
        # preciso verificar as horas.

        # Se a hora atual é maior do que a hora de início e menor do que a hora de fim, posso mostrar
        # sem verificar os minutos
        if date_and_times['start']['hour'] < date_and_times['now']['hour'] < date_and_times['end']['hour']:
            return True

        # Sei que posso mostrar pela hora, pois já passou da hora
        # de início da postagem, não preciso verificar mais as horas
        # e minutos de início, somente de fim
        if date_and_times['start']['hour'] < date_and_times['now']['hour']:
            if date_and_times['end']['hour'] >= date_and_times['now']['hour'] and date_and_times['end']['minute'] > \
                    date_and_times['now']['minute']:
                # Não preciso verificar os minutos, pois sei que
                # não vai terminar nessa hora ainda.
                return True

        #  Se a hora de início é a mesma da atual, preciso verificar
        #  os minutos de início e fim
        if date_and_times['start']['hour'] == date_and_times['now']['hour']:
            # Só mostro se a o minuto de início for o mesmo ou menor que o minuto atual
            if date_and_times['start']['minute'] <= date_and_times['now']['minute']:
                # Se a hora de fim não a mesma de agora, posso mostrar sem verificar os minutos
                if date_and_times['end']['hour'] > date_and_times['now']['hour']:
                    # Sei que posso mostrar pois não vai terminar nessa hora ainda, então não
                    # preciso verificar os minutos de fim
                    return True
                # Preciso verificar os minutos de fim, pois a hora atual já é a hora de fim
                # Se os minutos de fim forem maiores do que o minuto atual, posso mostrar
                elif date_and_times['end']['minute'] > date_and_times['now']['minute']:
                    return True

    return False


def _getSumDate(date_object):
    return date_object.year + date_object.month + date_object.day


def _getDateAndTimes(start_datetime, end_datetime, now_datetime) -> dict:
    object_with_dates = {
        'now': {
            'date_sum': _getSumDate(now_datetime),
            'hour': now_datetime.hour,
            'minute': now_datetime.minute
        },
        'start': {
            'date_sum': _getSumDate(start_datetime),
            'hour': start_datetime.hour,
            'minute': start_datetime.minute
        },
        'end': {
            'date_sum': _getSumDate(end_datetime),
            'hour': end_datetime.hour,
            'minute': end_datetime.minute
        },
    }

    return object_with_dates


def same_list(l1, l2):
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
    os.remove(filename)


def get_folder_filenames(folder_path: str) -> list:
    return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]


def create_filename(file_name: str, extension: str) -> str:
    return file_name.replace(' ', '-') + '.' + extension
