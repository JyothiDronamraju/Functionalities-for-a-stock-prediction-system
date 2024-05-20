import datetime
import requests

# implementing functions to load data from alpha vantage
api_key = 'HSAJMVL9SLP07ECB'

# function to load historical stock prices for given symbol
def load_stock_data(symbol, start_date, end_date):
    api_key = 'HSAJMVL9SLP07ECB'
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'
    response = requests.get(url)
    data = response.json()
    stock_data = data['Time Series (Daily)']
    stock_prices = []
    
    # calculate start date 20 years ago
    ten_years_ago = datetime.datetime.now() - datetime.timedelta(days=365*10)
    
    for date, price in stock_data.items():
        if ten_years_ago <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date:
            stock_prices.append(float(price['4. close']))

    return stock_prices

# load news_sentiment
def laod_news_sentiment(symbol):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data

# print(load_stock_data('AAPL', datetime.datetime(2010, 1, 1), datetime.datetime(2020, 1, 1))[0:5])

print(laod_news_sentiment('AAPL'))