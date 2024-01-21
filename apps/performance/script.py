import pandas

from blackbox.ticker import Ticker
from blackbox.chart import Chart
from lagoon.models.base import insert_batch
from lagoon.models.tickers.tickers_ignored import TickerIgnored
from w_scripts.performance import performance_accumulated
from apps.performance.config import LIST, LIST_GENERAL

from apps.performance.subscript import search_tickers_by_source

from lagoon.constants import SOURCE_BINANCE


def execute():
    for item_performance in LIST:
        # for item_performance in LIST_GENERAL:
        if not item_performance['active']:
            continue

        # ToDo:: Add name of parameter processing

        dataframe = pandas.DataFrame()

        input_search = item_performance['input']['search']
        input_date = item_performance['input']['search']['date']
        id_type_asset = item_performance['input']['search']['type_asset']
        id_source = item_performance['input']['search']['source']
        output_plot = item_performance['output']['plot']

        input_list: list = item_performance['input']['list']
        if not input_list:
            input_list = search_tickers_by_source(input_search)

        print('tickers to process::', len(input_list))
        print([item['ticker'] for item in input_list])

        list_tickers_error = []
        list_tickers_ignored = []
        first_date_dataframe = None

        for item in input_list:
            # ticker_name, id_source = item['ticker'], item['source']
            ticker_name = item['ticker']
            try:
                # Check names with '_x' and '_y'
                ticker = Ticker(ticker_name, id_source)
                optionals = item.get('optionals', None)
                ticker_serie = ticker.get_closing_data(dates=input_date, optionals=optionals)

                if dataframe.empty:
                    dataframe = ticker_serie
                    first_date_dataframe = dataframe.first_valid_index()
                    continue

                # ToDo:: Refactor
                if id_source == SOURCE_BINANCE and first_date_dataframe != ticker_serie.first_valid_index():
                    continue

                # ToDo:: FutureWarning:
                #  Passing 'suffixes' which cause duplicate columns {'LITUSDT_x'} in the result is deprecated and will raise a MergeError in a future version.
                #  dataframe = pandas.merge(left=dataframe, right=ticker_serie, how='inner', right_index=True, left_index=True)
                dataframe = pandas.merge(left=dataframe, right=ticker_serie, how='inner', right_index=True,
                                         left_index=True)

            except Exception as m:
                # ToDo:: Hacer una Exception generica como BlueOceanException, BlackboxException or Lagoon
                # ToDo:: Para hacer captura de excepcion global o negocio y dejar Exception para errores ajenos a la App.
                list_tickers_ignored.append(TickerIgnored(ticker=ticker_name,
                                                         id_source=id_source,
                                                         id_type=id_type_asset,
                                                         description=m.message))

        print('tickers with errors for ignored::', len(list_tickers_ignored))
        if list_tickers_ignored:
            insert_batch(list_tickers_ignored)

        # ToDo:: Review that point with CER because data is saving accumulated on BD.
        dataframe = performance_accumulated(dataframe, item_performance['output']['top'])

        chart = Chart(output_plot['title'])
        chart.add_plot(dataframe, input_list)
        chart.save(output_plot['name_to_save'])
