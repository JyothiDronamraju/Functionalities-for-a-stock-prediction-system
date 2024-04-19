from flask import Flask, render_template, request
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the model
look_back = 360
scaler = MinMaxScaler()
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(look_back, 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')
# model.load_weights("model_weights.h5")

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ticker = request.form["ticker"]
        stock_data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        stock_data['Close'] = stock_data['Close'].fillna(method='ffill')
        ts_data = stock_data['Close'].values.reshape(-1, 1)
        ts_data_normalized = scaler.fit_transform(ts_data)
        
        X, y = [], []
        for i in range(len(ts_data_normalized)-look_back-1):
            X.append(ts_data_normalized[i:(i+look_back), 0])
            y.append(ts_data_normalized[i + look_back, 0])
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        model.fit(X, y, epochs=10, batch_size=32)
        
        future_periods = 30
        future_predictions_normalized = []
        x_input = ts_data_normalized[-look_back:]
        for i in range(future_periods):
            x_input_reshaped = x_input.reshape((1, look_back, 1))
            future_prediction_normalized = model.predict(x_input_reshaped)[0, 0]
            future_predictions_normalized.append(future_prediction_normalized)
            x_input = np.append(x_input[1:], future_prediction_normalized)
        
        future_predictions = scaler.inverse_transform(np.array(future_predictions_normalized).reshape(-1, 1)).flatten()
        last_date = stock_data.index[-1]
        future_dates = pd.date_range(start=last_date, periods=future_periods+1, freq='D')[1:]
        
        plt.figure(figsize=(12, 6))
        plt.plot(stock_data.index[-60:], stock_data['Close'][-60:], label='Actual', color='blue')
        plt.plot(future_dates, future_predictions, label='Predicted', color='red')
        plt.title(f"Stock Price Prediction for {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.savefig("static/plot.png")
        plt.close()
        
        return render_template("index.html", plot="plot.png")
    
    return render_template("./index.html")

if __name__ == "__main__":
    app.run(debug=True)
