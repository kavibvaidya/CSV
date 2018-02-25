
#
# Ingest stock csv files to create a zipline data bundle

import os

import numpy  as np
import pandas as pd
import datetime

boDebug=True # Set True to get trace messages

from zipline.utils.cli import maybe_show_progress

def viacsv(symbols,start=None,end=None):


    # strict this in memory so that we can reiterate over it.
    # (Because it could be a generator and they live only once)
    tuSymbols = tuple(symbols)

    if boDebug:
        print("entering viacsv.  tuSymbols=",tuSymbols)

    # Define our custom ingest function
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,  # unused
               daily_bar_writer,
               adjustment_writer,
               calendar,
               cache,
               show_progress,
               output_dir,
               # pass these as defaults to make them 'nonlocal' in py2
               start=start,
               end=end):

        produce(tuSymbols)

        if boDebug:
            print("entering ingest and creating blank dfMetadata")

        dfMetadata = pd.DataFrame(np.empty(len(tuSymbols), dtype=[
            ('start_date', 'datetime64[ns]'),
            ('end_date', 'datetime64[ns]'),
            ('auto_close_date', 'datetime64[ns]'),
            ('symbol', 'object'),
        ]))

        if boDebug:
            print("dfMetadata",type(dfMetadata))
            print(dfMetadata.describe)
            print()

        # We need to feed something that is iterable - like a list or a generator -
        # that is a tuple with an integer for sid and a DataFrame for the data to
        # daily_bar_writer

        liData=[]
        iSid=0
        for S in tuSymbols:
            IFIL="~/documents/CSV/"+S+".csv"
            if boDebug:
               print("S=",S,"IFIL=",IFIL)
            dfData=pd.read_csv(IFIL,index_col=0,parse_dates=True).sort_index()
            print("what")
            if boDebug:
               print("read_csv dfData",type(dfData),"length",len(dfData))
               print()
            dfData.rename(
                columns={
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Close': 'close',
                    'Volume': 'volume',
                    'Adj Close': 'price',
                },
                inplace=True,
            )
            dfData['volume']=dfData['volume']/1000
            liData.append((iSid,dfData))

            # the start date is the date of the first trade and
            start_date = dfData.index[0]
            if boDebug:
                print("start_date",type(start_date),start_date)

            # the end date is the date of the last trade
            end_date = dfData.index[-1]
            if boDebug:
                print("end_date",type(end_date),end_date)

            # The auto_close date is the day after the last trade.
            ac_date = end_date + pd.Timedelta(days=1)
            if boDebug:
                print("ac_date",type(ac_date),ac_date)

            # Update our meta data
            dfMetadata.iloc[iSid] = start_date, end_date, ac_date, S

            iSid += 1

        if boDebug:
            print("liData",type(liData),"length",len(liData))
            print(liData)
            print()
            print("Now calling daily_bar_writer")

        daily_bar_writer.write(liData, show_progress=False)

        # Hardcode the exchange to "YAHOO" for all assets and (elsewhere)
        # register "YAHOO" to resolve to the NYSE calendar, because the csv files
        # are for equities that traded per the NYSE calendar.
        dfMetadata['exchange'] = "Alpha_vantage"

        if boDebug:
            print("returned from daily_bar_writer")
            print("calling asset_db_writer")
            print("dfMetadata",type(dfMetadata))
            print(dfMetadata)
            print()

        # Not sure why symbol_map is needed
        symbol_map = pd.Series(dfMetadata.symbol.index, dfMetadata.symbol)
        if boDebug:
            print("symbol_map",type(symbol_map))
            print(symbol_map)
            print()

        asset_db_writer.write(equities=dfMetadata)

        if boDebug:
            print("returned from asset_db_writer")
            print("calling adjustment_writer")

        adjustment_writer.write()

        if boDebug:
            print("returned from adjustment_writer")
            print("now leaving ingest function")

    if boDebug:
       print ("about to return ingest function")
    return ingest


#This is suppossed to be nother file, but it is not so for typing purposes.
import requests
import pandas as pd
import csv, argparse

def produce(symbols):
    for symbol in symbols:
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&outputsize=full&apikey=DK1XS6X3NJ8R5F0O&datatype=csv"
        response = requests.get(url)
        # Print the status code of the response.
        #print(response.text)

        parser = csv.reader(response.text.split('\n'))
        #converts the requests into csv file
        f = open("/Users/Vaidya/documents/CSV/" + symbol+ ".csv", "w+")
        writer = csv.writer(f)
        count =0
        for i in parser:
            if count == 0:
                i[0] = "date"
            if len(i) != 0 and count < 750:
                writer.writerow((i[0], i[1],i[2],i[2],i[3],i[4],i[6],i[5]))
            count +=1
        f.close()
