import pandas as pd
import zipline
from zipline import *
from collections import OrderedDict
import pytz

def initialize():
    pass

def handle_data():
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))

datas = OrderedDict()

datas["results"] = pd.read_csv("result.csv", index_col=0, parse_dates=['timestamp'])
panel = pd.Panel(datas)

algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data, capital_base = 100000.0)
#run algo
perf_manual = algo_obj.run(datas)
