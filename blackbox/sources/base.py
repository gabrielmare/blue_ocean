class SourceBase:
    __requests_done = 0

    @staticmethod
    def __make_request(endpoint, ticker=None):
        pass

    @staticmethod
    def __list(type_asset: str = None):
        pass

    @staticmethod
    def __wait_not_so_fast():
        SourceBase.__requests_done += 1
        pass

    @staticmethod
    def __standarize_fields_v2(data: dict, fields_to_convert: dict):
        pass

    @staticmethod
    def historical(ticker: str, dates: dict = None, optionals: dict = None):
        pass
