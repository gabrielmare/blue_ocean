import pandas

from blackbox.sources.tools.exceptions import SourceNotFound
from blackbox.sources import SOURCES, PARAMS_BY_SOURCE


class Ticker:
    name: str
    id_source: int
    source = None
    data = None
    dataframe = None
    closing_data = None

    def __init__(self, name: str, id_source: int):
        if id_source not in SOURCES.keys():
            raise SourceNotFound(id_source)

        self.name = name
        self.id_source = id_source

        # Applying Dependency Injection to set Source's type.
        self.source = SOURCES[self.id_source]

    def historical(self, dates: dict = None, optionals: dict = None):
        # Si no tengo los datos historic del ticker, los busco por la fuente
        if not self.data:
            self.data = self.source.historical(self.name, dates=dates, optionals=optionals)

        return self.data

    def get_dataframe(self, dates=None, optionals: dict = None):
        # Sino tengo el Dataframe del ticker, lo creo.
        if not self.dataframe:
            # Sino tengo los datos historicos del ticker, los busco.
            if not self.data:
                self.historical(dates, optionals)

            # Teniendo el historio de datos puedo generar el dataframe
            self.dataframe = pandas.DataFrame(self.data)
            # Conversion de fecha de string a Datetime
            self.dataframe['date'] = pandas.to_datetime(self.dataframe['date'], format=PARAMS_BY_SOURCE[self.id_source]['format_date_response'], utc=False)
            self.dataframe.set_index(keys=['date'], drop=True, inplace=True)
            self.dataframe.index.name = 'date'
            # Elimino los posibles indices duplicados
            self.dataframe = self.dataframe.groupby(self.dataframe.index).first()
            # Por defecto, ordenamiento de fecha ascendente.
            self.dataframe.sort_index(ascending=True, inplace=True)

        return self.dataframe

    def get_closing_data(self, dates=None, optionals: dict = None):
        # Si no tengo los datos de cierre, creo la serie
        if not self.closing_data:
            # Sino tengo el Dataframe del ticker, lo creo.
            if not self.dataframe:
                self.get_dataframe(dates, optionals)

            if 'close' in self.dataframe.columns:
                # Teniendo el dataframe puedo generar los datos de cierre
                self.closing_data = pandas.Series(data=self.dataframe['close'],
                                                  index=self.dataframe.index.values)
            else:
                self.closing_data = self.dataframe.squeeze()

            self.closing_data.name = self.name
            self.closing_data.index.name = 'date'

        return self.closing_data
