import requests
import pandas as pd
import csv, argparse

def produce(symbol):
	url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=DK1XS6X3NJ8R5F0O&datatype=csv"
	response = requests.get(url)
	# Print the status code of the response.
	#print(response.text)

	parser = csv.reader(response.text.split('\n'))
	#converts the requests into csv file
	f = open('./.gitignore/result.csv', "w")
	writer = csv.writer(f)
	count =0
	for i in parser:
		if len(i) != 0:
			writer.writerow((i[1],i[2],i[2],i[3],i[4],i[6],i[5]))

	f.close()


produce("AAPL")
