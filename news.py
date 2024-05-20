import yfinance as yf

# Define the stock ticker symbol
ticker_symbol = "AAPL"

#print latest news
stock = yf.Ticker(ticker_symbol)
news = stock.news
print(news)