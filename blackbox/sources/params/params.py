import json

from blackbox.sources.params.base import PARAMS
from blackbox.sources.params.sources import SOURCES


class Params:
    def __init__(self):
        self.__params_base = PARAMS
        self.__params_sources = SOURCES

    def get_by_source(self, source):
        # Source exits and have params/value, return their params
        if source in self.__params_sources.keys() and self.__params_sources[source]:
            return self.__params_sources[source]

        # Return params/values of default source
        return self.__params_sources[self.__params_sources['default']]

    def get_backbox_params(self):
        return self.__params_base['blackbox']

    def get_header_params(self):
        return self.__params_base['header']


o_params = Params()
blackbox_params = o_params.get_backbox_params()
HEADER = o_params.get_header_params()
FORMAT_DATE_BLACKBOX = blackbox_params['format_date']
DEFAULT_DATES = blackbox_params['default_dates']
