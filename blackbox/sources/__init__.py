from blackbox.sources.iol import IOL, params_iol
from blackbox.sources.nasdaq import Nasdaq, params_nasdaq
from blackbox.sources.bcra import BCRA, params_bcra
from blackbox.sources.binance import Binance, params_binance
from lagoon.constants import *

SOURCES = {
    SOURCE_NASDAQ: Nasdaq(),
    SOURCE_BINANCE: Binance(),
    SOURCE_IOL: IOL(),
    SOURCE_BCRA: BCRA()
}

PARAMS_BY_SOURCE = {
    SOURCE_NASDAQ: params_nasdaq,
    SOURCE_BINANCE: params_binance,
    SOURCE_IOL: params_iol,
    SOURCE_BCRA: params_bcra
}

__all__ = ['SOURCES', 'PARAMS_BY_SOURCE', 'IOL', 'Nasdaq', 'BCRA', 'Binance']
