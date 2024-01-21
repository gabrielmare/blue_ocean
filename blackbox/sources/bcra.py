from blackbox.sources.params.params import o_params, HEADER
from blackbox.sources.base import SourceBase
from blackbox.sources.tools.tools import *
from blackbox.sources.tools.exceptions import SourceAPIException

params_bcra = o_params.get_by_source(t_get_only_module_name(__name__))
endpoints_bcra = params_bcra['endpoints']


class BCRA(SourceBase):
    __name__ = 'bcra'

    def __make_request(self, endpoint, ticker=None):
        json_response = {}
        try:
            # self.__wait_not_so_fast()
            header = HEADER
            header['Authorization'] = params_bcra['authorization']

            response = requests.get(endpoint, headers=header)
            json_response = response.json()
            if response.status_code != 200:
                raise SourceAPIException(self.__name__, ticker, response.status_code, json_response['Message'], json_response['MessageDetail'])
        except Exception as ex:
            print(ex)

        return json_response

    def __standarize_fields_v2(self, data: dict, fields_input_output: dict):
        response = {}
        for field_input, field_output_tuple in fields_input_output.items():
            output_name, output_convert_to = field_output_tuple[0], field_output_tuple[1]
            if output_name == 'date':
                part_date = str(data[field_input]).split('-')
                response[output_name] = f'{part_date[2]}/{part_date[1]}/{part_date[0]}'
            else:
                response[output_name] = data[field_input]
        return response

    def historical(self, ticker: str, dates: dict = None, optionals: dict = None):
        response = []

        # Fixing endpoint
        data_endpoint = endpoints_bcra[ticker]
        endpoint = t_get_full_endpoint(params_bcra['domain'], data_endpoint['url'])

        data = self.__make_request(endpoint, ticker)

        for row in data:
            standarize_fields = self.__standarize_fields_v2(row, data_endpoint['fields_input_output_V2'])
            if standarize_fields:
                response.append(standarize_fields)

        # Filter by n last periods
        if dates and dates['periods']:
            start_index = len(response) - dates['periods']
            return response[start_index:]

        # Filter by start and end dates
        if dates and dates['start'] and dates['end']:
            return response[dates['start']:dates['end']]

        return response
