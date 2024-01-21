from blackbox.sources.params.params import o_params, HEADER
from blackbox.sources.base import SourceBase
from blackbox.sources.tools.tools import *
from blackbox.sources.tools.exceptions import SourceAPIException, NotAllowedDataException

params_iol = o_params.get_by_source(t_get_only_module_name(__name__))
endpoints_iol = params_iol['endpoints']


class IOL(SourceBase):
    __name__ = 'iol'

    def __make_request(self, endpoint, ticker=None):
        json_response = {}
        try:
            # self.__wait_not_so_fast()
            response = requests.get(endpoint, headers=HEADER)
            json_response = response.json()
            if response.status_code != 200:
                raise SourceAPIException(self.__name__, ticker, response.status_code, json_response['Message'], json_response['MessageDetail'])
        except Exception as ex:
            print(ex)

        return json_response

    def __standarize_fields_v2(self, data: dict, fields_to_convert: dict):
        response = {}
        for input_name, field_output_tuple in fields_to_convert.items():
            output_name, output_type = field_output_tuple[0], field_output_tuple[1]
            response[output_name] = t_epoch_to_str(data[input_name]) \
                if output_name == 'date' else t_cast_value(data[input_name], output_type)
        return response

    def list(self, type_asset: str = None):
        pass

    def historical(self, ticker: str, dates: dict = None, optionals: dict = None):
        response = []
        period = optionals['period'] if optionals and optionals['period'] else 'D'

        # Fixing endpoint
        data_endpoint = endpoints_iol['historical']
        start_date, end_date = t_get_dates_epoch(dates, params_iol['format_date_request'])
        query = data_endpoint['query'].replace('TICKER', ticker).replace('FROM_DATE_INT', start_date).\
            replace('TO_DATE_INT', end_date).replace('PERIOD', period.upper())
        endpoint = t_get_full_endpoint(params_iol['domain'], data_endpoint['url'], query)

        data = self.__make_request(endpoint, ticker)

        if data[data_endpoint['output_data_root']]:
            for row in data[data_endpoint['output_data_root']]:
                standarize_fields = self.__standarize_fields_v2(row, data_endpoint['fields_input_output_V2'])
                if standarize_fields:
                    response.append(standarize_fields)

        return response
