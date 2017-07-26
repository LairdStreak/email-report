
from datetime import datetime
from pandas import DataFrame
import pandas_datareader.data as web
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

""" grab stock data for a suite of coumpanies I am interested in
	take this data and return a few graphs and tables. """

#build a list of the stocks you care about

def get_american_stock_dat(stock_of_interest, start_time, now_time):
	#use the below to build up a dataframe of the current price,
	#a graph of the past year and a the close vs. this time a month ago
	f_dat = web.DataReader(stock_of_interest, 'google', start_time, now_time)
	#then use below to get the dataframe for a specific stock
	return f_dat

def TSE_current_price(stock):
	google_price_api = 'http://finance.google.com/finance/info?client=ig&q=TSE%3A'
	current_price_api = google_price_api+stock
	stock_dat_now = urlopen(current_price_api)
	now_price = BeautifulSoup(stock_dat_now, 'lxml')
	dict_string = [x for x in now_price.body.p.children][0]
	t_1 = dict_string.split('[\n')[1]
	t_2 = t_1.split('\n]')[0]
	parsed_now_price = json.loads(t_2)

	# 't' is ticker name
	# 'l' == last price
	return (parsed_now_price['t'], parsed_now_price['l'])

def TSE_last_month_prices(stock):
	""" return a dataframe with the dates and the closing prices """
	google_historical_price_site= 'https://www.google.ca/finance/historical?q=TSE%3A'
	historical_price_page = google_historical_price_site + stock
	stock_dat = urlopen(historical_price_page)
	#then parse the tbale with BS and call the next page with the crawler

	historical_page = BeautifulSoup(stock_dat,'lxml')

	table_dat = historical_page.find('table',{'class':'gf-table historical_price'})
	#gets the table for last 30 trading days
	#look at the textbook for parsing of tables! we are right there :D
	#4th column is close - this is the one we care about
	rows = table_dat.findAll('td',{'class':'lm'})
	dates = [x.get_text() for x in rows]
	prices = []
	for row in rows:
		for i, j in enumerate(row.next_siblings):
			if i == 3:
				prices.append(j.get_text())
	dates = [date.rstrip() for date in dates]
	prices = [price.rstrip() for price in prices]
	outdat = DataFrame(list(zip(dates,prices)),columns = ['Date','Close'])
	return outdat


if __name__ == '__main__':

	now_time = datetime.now()

	start_time = datetime((now.year ), now.month - 1, now.day)

	stocks_of_interest = ['AMZN','GOOG','AAPL','CLDR','HDP','ORCL','TSLA']

	for stock in stocks_of_interest:
		#scrape the stock data to a df
		stock_df = stock_data.get_american_stock_dat(stock,start_time, now_time )
		#plot the stock df 
		graph_of_close = stock_graph.plot_us_stock_data(stock_df, stock)
		#take the plot and add it to the email message
		graph_to_message_body(graph_of_close, message_body)



	canadian_stocks_of_interest = ['BEP.UN','EXE','FC','TXF','XWD','VCN','VFV','VUN']
	
	stock_prices = []
	for stock in canadian_stocks_of_interest:
		now = stock_data.TSE_current_price(stock)
		stock_prices.append(now)
		#scrape the stock data to a df
		price_df = stock_data.TSE_last_month_prices(stock)
		#plot the stock df 
		graph_of_close = stock_graph.plot_cad_stock_data(price_df, stock)
		#take the plot and add it to the email message
		graph_to_message_body(graph_of_close, message_body)


	





