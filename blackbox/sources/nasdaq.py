from blackbox.sources.params.params import o_params, HEADER
from blackbox.sources.base import SourceBase
from blackbox.sources.tools.tools import *
from blackbox.sources.tools.exceptions import SourceAPIException, NotAllowedDataException

params_nasdaq = o_params.get_by_source(t_get_only_module_name(__name__))
endpoints_nasdaq = params_nasdaq['endpoints']


class Nasdaq(SourceBase):
    __name__ = 'nasdaq'

    def __make_request(self, endpoint, ticker=None):
        json_response = {}
        try:
            # self.__wait_not_so_fast()
            response = requests.get(endpoint, headers=HEADER)
            json_response = response.json()
            if response.status_code != 200 or json_response['status']['rCode'] != 200:
                first_status = json_response['status'][0]
                raise SourceAPIException(self.__name__, ticker, response.status_code, first_status['bCodeMessage'],
                                         first_status['errorMessage'])
            json_response = json_response['data']
        except Exception as m:
            pass
            # if json_response and json_response['status']:
            #     # m = f"status: {json_response['status']['rCode']} - message: {json_response['status']['bCodeMessage'][0]['errorMessage']}"
            #     m = f"{json_response['status']['bCodeMessage'][0]['errorMessage']}"
            # print(ticker, m)

        return json_response

    def __get_recursive_value_v2(self, data, input_field: str):
        if isinstance(data, dict):
            if input_field in data.keys():
                return data[input_field]

            for next_level_value in data.values():
                if isinstance(next_level_value, dict) or isinstance(next_level_value, list):
                    return self.__get_recursive_value_v2(next_level_value, input_field)

        elif isinstance(data, list):
            for item in data:
                return self.__get_recursive_value_v2(item, input_field)

    def __standarize_fields_v2(self, data, fields_input_output):
        response = {}
        for field_input, field_output_tuple in fields_input_output.items():
            output_name, output_convert_to = field_output_tuple[0], field_output_tuple[1]
            # value = Nasdaq.__get_recursive_value_v2(data, field_input)
            value = data[field_input]
            response[output_name] = t_cast_value(value, output_convert_to)
        return response

    def list(self, type_asset: str = None):
        # ToDo:: Change dict_response for obj list, same format response with historical method
        list_response = []

        data_endpoint = endpoints_nasdaq['list']
        if type_asset not in data_endpoint.keys():
            raise NotAllowedDataException('The type asset ' + type_asset + '.')

        data_endpoint = data_endpoint[type_asset]
        endpoint = t_get_full_endpoint(params_nasdaq['domain'], data_endpoint['url'], data_endpoint['query'])

        data = self.__make_request(endpoint, type_asset)

        if data:
            # Limpieza general de datos
            data_clean_json = t_clear_data(data, params_nasdaq['characters_not_allowed'])
            rows = self.__get_recursive_value_v2(data_clean_json, data_endpoint['output_data_root'])
            for row in rows:
                custom_fields = self.__standarize_fields_v2(row, data_endpoint['fields_input_output_V2'])
                if custom_fields:
                    list_response.append({'ticker': custom_fields['ticker'], 'name': custom_fields['name'],
                                          'close': custom_fields['close'], 'source': self.__name__})

        return list_response

    def historical(self, ticker: str, dates: dict = None, optionals: dict = None):
        response = []
        # try:
        type_asset = optionals['type_asset'] if optionals and optionals['type_asset'] else 'stocks'

        # Fixing endpoint
        data_endpoint = endpoints_nasdaq['historical']
        start_date, end_date = t_get_dates(dates, params_nasdaq['format_date_request'])
        url = data_endpoint['url'].replace('TICKER', ticker)
        query = data_endpoint['query'].replace('TYPE_ASSET', type_asset) \
            .replace('FROM_DATE', start_date).replace('TO_DATE', end_date).replace('LIMIT', str(params_nasdaq['limit']))
        endpoint = t_get_full_endpoint(params_nasdaq['domain'], url, query)

        data = self.__make_request(endpoint, ticker)

        # if data and data[data_endpoint['output_data_root']]:
        if data:
            # Limpieza general de datos
            # rows = json.loads(t_clear_text(json.dumps(data[data_endpoint['output_data_root']]['rows'])))
            data_clean_json = t_clear_data(data, params_nasdaq['characters_not_allowed'])
            rows = self.__get_recursive_value_v2(data_clean_json, data_endpoint['output_data_root'])
            for row in rows:
                standarize_fields = self.__standarize_fields_v2(row, data_endpoint['fields_input_output_V2'])
                if standarize_fields:
                    response.append(standarize_fields)
        # except Exception as ex:

        return response
