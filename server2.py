import requests
from sklearn.ensemble import RandomForestClassifier

api_key = 'HSAJMVL9SLP07ECB'
symbol = 'IBM'

# Make the API call
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&datatype=csv&outputsize=full'
response = requests.get(url)

# Save the data to a file
with open('aapl.csv', 'w') as f:
  f.write(response.text)

# Read the data from the file
import pandas as pd
df = pd.read_csv('aapl.csv')

# Print the data
df = df.set_index('timestamp')

df = df.iloc[::-1]

df["tomorrow"] = df["close"].shift(-1)
df["target"] = (df["tomorrow"] > df["close"]).astype(int)

model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)

train = df.iloc[:-100]
test = df.iloc[-100:]

predictors = ["close", "volume", "open", "high", "low"]

model.fit(train[predictors], train["target"])


def predict(train, test, predictors, model):
    model.fit(train[predictors], train["target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="predictions")
    combined = pd.concat([test["target"], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    
    return pd.concat(all_predictions)


horizons = [2,5,60,250,1000]
new_predictors = []

for horizon in horizons:
    rolling_averages = df.rolling(horizon).mean()
    
    ratio_column = f"close_ratio_{horizon}"
    df[ratio_column] = df["close"] / rolling_averages["close"]
    
    trend_column = f"trend_{horizon}"
    df[trend_column] = df.shift(1).rolling(horizon).sum()["target"]
    
    new_predictors+= [ratio_column, trend_column]

df = df.dropna(subset=df.columns[df.columns != "tomorrow"])

model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
predictions = backtest(df, model, new_predictors)

predictions = backtest(df, model, new_predictors)
print(predictions)