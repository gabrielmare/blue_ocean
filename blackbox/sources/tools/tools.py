import datetime
import time
import requests
import pandas
import json
from blackbox.sources.tools.exceptions import FormatDateIncorrectException
from blackbox.sources.params.params import FORMAT_DATE_BLACKBOX, DEFAULT_DATES


def t_get_only_module_name(name: str):
    return name.split('.')[-1]


def t_get_full_endpoint(domain: str, url: str, query: str = None):
    if query:
        return '{0}{1}{2}'.format(domain, url, query)
    return '{0}{1}'.format(domain, url)


def t_clear_data(data, characters_to_exclude: list = None):
    if not characters_to_exclude:
        return data

    data_str = json.dumps(data)
    for character in characters_to_exclude:
        data_str = data_str.replace(character, '')
    data = json.loads(data_str)

    return data


def t_cast_value(value, type_to_convert):
    if not type_to_convert:
        return value

    try:
        if type_to_convert == 'float':
            return round(float(str(value)), 2)

        if type_to_convert == 'int':
            return int(str(value).replace(',', ''))

    except ValueError:
        return 0


def t_formating_date(input_date, format_date):
    try:
        l_date = input_date.split('/')
        str_date = datetime.datetime(l_date[0], l_date[1], l_date[2])
        return str_date.strftime(format_date)
    except FormatDateIncorrectException as ex:
        print(ex)


def t_str_to_epoch(str_date, format_date):
    return str(int(time.mktime(time.strptime(str_date, format_date))))


def t_from_date_by_period(today, days: int, format_date: str):
    """
    Calculate FROM/START date between today and minus period/days.
    :param today:
    :param days:
    :param format_date:
    :return:
    """
    return (today - datetime.timedelta(days)).strftime(format_date)


def t_epoch_to_str(numeric_date):
    """
    Convert Epoch date to string BlackBox format dd/mm/yyyy.
    :param numeric_date:
    :return:
    """
    if isinstance(numeric_date, str):
        numeric_date = float(numeric_date)
    return datetime.datetime.fromtimestamp(numeric_date).strftime(FORMAT_DATE_BLACKBOX)


def t_get_dates(date: dict, format_by_source: str):
    if date and date['start'] and date['end']:
        return t_formating_date(date['start'], format_by_source), t_formating_date(date['start'], format_by_source)

    today = datetime.datetime.today()
    periods = date['periods']+1 if date and date['periods'] else DEFAULT_DATES['periods']

    return t_from_date_by_period(today, periods, format_by_source), today.strftime(format_by_source)


def t_get_dates_epoch(date: dict, format_by_source: str):
    if date and date['start'] and date['end']:
        return t_str_to_epoch(date['start'], format_by_source), t_str_to_epoch(date['end'], format_by_source)

    today = datetime.datetime.today()
    today_epoch = t_str_to_epoch(today.strftime(format_by_source), format_by_source)
    periods = date['periods']+1 if date and date['periods'] else DEFAULT_DATES['periods']+1
    start_date = t_from_date_by_period(today, periods, format_by_source)

    return t_str_to_epoch(start_date, format_by_source), today_epoch
