# Dada un ticker o una lista de tickers pintar un grafico de barras/lineas
import matplotlib.pyplot
import pandas


class Chart:
    __figure: matplotlib.pyplot.Figure = None
    __main_axes: matplotlib.pyplot.Axes = None

    def __init__(self, title):
        self.__figure, self.__main_axes = matplotlib.pyplot.subplots(figsize=(10, 8),
                                                                     layout='constrained')
        self.__main_axes.set_title(title)

    def add_plot(self, data_processed, data_original: list, y_label: str = None, legend: bool = True):
        if isinstance(data_processed, pandas.DataFrame):
            for column in data_processed.columns:
                alias = None
                for c_ticker in data_original:
                    # ToDo:: Review alias
                    if c_ticker['ticker'] == column:
                        alias = c_ticker.get('alias', None)
                        break
                alias = f'{column}:: {alias}' if alias else column
                self.__main_axes.plot(data_processed.index.values, data_processed[column], label=alias)

        elif isinstance(data_processed, pandas.Series):
            self.__main_axes.plot(data_processed.index.values, data_processed, label=data_processed.name)

        if y_label:
            self.__main_axes.set(ylabel=y_label)

        if legend:
            self.__main_axes.legend()

        self.__main_axes.tick_params(axis='x', rotation=45)

    def show(self):
        self.__figure.show()

    def save(self, name: str):
        self.__figure.savefig(name)
