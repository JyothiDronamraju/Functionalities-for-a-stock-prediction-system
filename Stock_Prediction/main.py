import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from textblob import TextBlob  # For sentiment analysis

# Define the stock ticker symbol
ticker_symbol = "AAPL"

# Get historical market data for the stock
stock = yf.Ticker(ticker_symbol)
historical_data = stock.history(period="1y")

# Calculate daily returns
historical_data['Daily_Return'] = historical_data['Close'].pct_change()

# Calculate volatility (using 30-day standard deviation)
historical_data['Volatility'] = historical_data['Close'].rolling(window=30).std()

# Get dividends data
dividends = stock.dividends

# Create binary indicator for dividends
historical_data['Dividend'] = np.where(historical_data.index.isin(dividends.index), 1, 0)

# Perform sentiment analysis on recent news headlines
news = stock.news

news_sentiment = [TextBlob(c['title']).sentiment.polarity for c in news]
historical_data['News_Sentiment'] = np.mean(news_sentiment)


# Combine all features into a single dataframe
features = historical_data[['Daily_Return', 'Volatility', 'Dividend', 'News_Sentiment']]

# Add target variable (next quarter's return)
features['Next_Quarter_Return'] = features['Daily_Return'].shift(-90)

# Drop rows with NaN values (due to shift for target variable)
features = features.dropna()

# Split data into training and testing sets
X = features.drop('Next_Quarter_Return', axis=1)
y = features['Next_Quarter_Return']

# Use the data for training and evaluating a model (e.g., regression model)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("Training score:", train_score)
print("Testing score:", test_score)

