from apps.performance.constants import NASDAQ_EXCLUDE_TICKERS
from blackbox.sources import SOURCES, Binance, Nasdaq
from lagoon.constants import *
from lagoon.models.tickers.tickers_ignored import TickerIgnored


def filter_custom_binance(list_data: list, filters: dict) -> list:
    return_list, ticker_list = [], []
    concatenate_to_name = filters['concatenate_to_name'] if filters['concatenate_to_name'] else ' '
    remove_names_with = filters['remove_names_with']
    func_price = filters['func_price']

    # Get all tickers ignored from Lagoon.
    tickers_ignored = TickerIgnored.select_by_source(id_source=SOURCE_BINANCE)

    for item in list_data:

        ticker, close = item['ticker'], item['close']
        ticker_concatenated = ticker + concatenate_to_name

        # Validate not add tickers duplicated
        if ticker_concatenated in ticker_list:
            continue

        # Validate not add tickers excluded
        if ticker_concatenated in tickers_ignored:
            continue

        # Validate if ticker name contain words/characters not requirements
        if remove_names_with:
            flag_contains = False
            for word in remove_names_with:
                if word in ticker:
                    flag_contains = True
                    break
            if flag_contains:
                continue

        if func_price and not func_price(close):
            continue

        item['ticker'] = ticker_concatenated
        return_list.append(item)
        ticker_list.append(item['ticker'])

    return return_list


def filter_custom_nasdaq(list_data: list, filters: dict) -> list:
    return_list = []
    func_price = filters['func_price']
    number_tickets_to_process = filters['take_first']

    # Get all tickers ignored from Lagoon.
    tickers_ignored = TickerIgnored.select_by_source(id_source=SOURCE_NASDAQ)

    for item in list_data:

        ticker, close = item['ticker'], item['close']

        # if ticker in NASDAQ_EXCLUDE_TICKERS:
        if ticker in tickers_ignored:
            continue

        if func_price and not func_price(close):
            continue

        if number_tickets_to_process and number_tickets_to_process > 0:
            number_tickets_to_process -= 1
            if number_tickets_to_process == 0:
                break

        if not item['name']:
            item['name'] = ticker

        return_list.append(item)

    return return_list


def search_tickers_by_source(input_search: dict) -> list:
    id_source, type_asset = input_search['source'], input_search.get('type_asset', None)

    if id_source not in SOURCES.keys():
        # ToDo:: Review source not exists
        Exception('Source ' + id_source + 'not exists.')

    list_info_tickers: list = SOURCES[id_source].list(type_asset)

    if input_search['filter']:

        if id_source == SOURCE_BINANCE:
            list_info_tickers = filter_custom_binance(list_info_tickers, input_search['filter'])

        if id_source == SOURCE_NASDAQ:
            list_info_tickers = filter_custom_nasdaq(list_info_tickers, input_search['filter'])

    return list_info_tickers
