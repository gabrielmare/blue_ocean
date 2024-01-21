# ToDo:: Make a specific Exception to BlueOcean to Replace Exception
#           More specific with more data/description


class SourceNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str.format("{0} isn't source.", self.value)


class TickerNotFound(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str.format(self.message)


class SourceAPIException(Exception):

    def __init__(self, source, ticker, code, message, description):
        self.source = source
        self.ticker = ticker
        self.code = code
        self.message = message
        self.description = description

    def __str__(self):
        output = 'Source:: {0}'.format(self.source)

        if self.ticker:
            output += ' - Ticker:: {0}'.format(self.ticker)

        output += ' - StatusCode:: {0}'.format(self.code)

        if self.message:
            output += ' - Message:: {0}'.format(self.message)

        if self.description:
            output += ' - Description:: {0}'.format(self.description)

        return output


class FormatDateIncorrectException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str.format("Incorrect configured format date:: {0}", self.value)


class ReturnValueAPINasdaqException(Exception):
    def __init__(self, value):
        self.value = value


class NotAllowedDataException(Exception):
    __extra_data = ' Check config.'

    def __init__(self, value):
        self.value = value + self.__extra_data
