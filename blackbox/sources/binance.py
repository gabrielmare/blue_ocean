import json

from blackbox.sources.params.params import o_params, HEADER
from blackbox.sources.base import SourceBase
from blackbox.sources.tools.tools import *
from blackbox.sources.tools.exceptions import SourceAPIException, TickerNotFound

params_binance = o_params.get_by_source(t_get_only_module_name(__name__))
endpoints_binance = params_binance['endpoints']


class Binance(SourceBase):
    __name__ = 'binance'

    def __make_request(self, endpoint, ticker=None):
        list_response = []
        try:
            # self.__wait_not_so_fast()
            response = requests.get(endpoint, headers=HEADER)
            list_response = json.loads(response.text)
            # if response.status_code != 200:
            #     first_status = json_response['status'][0]
            #     raise SourceAPIException(self.__name__, ticker, response.status_code, first_status['bCodeMessage'],
            #                              first_status['errorMessage'])
            # json_response = json_response['data']
        except Exception as m:
            print(f"No tan rapido cerebrito:: {ticker}", m)

        return list_response

    def list(self, type_asset: str = None):
        list_response = []
        take = 1000

        endpoint_params = params_binance['endpoints']['list']

        for start in range(1, 10):
            skip = start if start == 1 else ((start - 1) * take) + 1
            query = endpoint_params['query'].replace('START', str(skip)).replace('LIMIT', str(take))
            endpoint = t_get_full_endpoint(params_binance['domain'], endpoint_params['url'], query)

            response = requests.get(endpoint, headers=HEADER)
            json_response = response.json()
            json_response = json_response['data']['body']['data']

            if not response or response.status_code != 200:
                print("status:: ", response.status_code)
                break

            for data in json_response:
                list_response.append({'ticker': data['symbol'], 'name': data['slug'].replace("'", "").replace('"', ''),
                                      'close': float(data['quote']['USD']['price']), 'source': self.__name__})

        return list_response

    def historical(self, ticker: str, dates: dict = None, optionals: dict = None):
        response = []

        optionals = {} if not optionals else optionals
        timeframe = optionals.get('TIMEFRAME', '1d')

        endpoint_params = params_binance['endpoints']['historical']

        # start_date, end_date = t_get_dates(dates, params_binance['format_date_request'])
        query = endpoint_params['query'].replace('PERIODS', str(dates['periods'])) \
            .replace('TICKER', ticker).replace('TIMEFRAME', str(timeframe))

        endpoint = t_get_full_endpoint(params_binance['domain'], endpoint_params['url'], query)

        data_list = self.__make_request(endpoint, ticker)

        """
        ToDo:: Look for what is each data on list...
                First value is data and I must be to convert
        """
        if data_list and isinstance(data_list, dict) and data_list['code'] and int(data_list['code']) < 0:
            raise TickerNotFound(data_list['msg'])

        for item in data_list:
            response.append({'date': t_epoch_to_str(str(item[0])[0:10]),
                             'open': float(item[1]),
                             'high': float(item[2]),
                             'low': float(item[3]),
                             'close': float(item[4])
                             })

        return response
