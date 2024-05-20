from flask import Flask, render_template, request
import numpy as np
import yfinance as yf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime, timedelta



app = Flask(__name__)

# Function to create a sliding window of data
def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:(i + window_size), 0])
        y.append(data[i + window_size, 0])
    return np.array(X), np.array(y)

@app.route('/', methods=['GET', 'POST'])
def predict_stock():
    if request.method == 'POST':
        symbol = request.form['symbol']
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        data = yf.download(symbol, start=start_date, end=end_date)['Close'].values.reshape(-1, 1)
        data_normalized = (data - np.min(data)) / (np.max(data) - np.min(data))
        window_size = 30
        X, y = create_dataset(data_normalized, window_size)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(window_size, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, epochs=2, batch_size=32)
        last_window = data_normalized[-window_size:].reshape(1, window_size, 1)
        predictions = []
        for _ in range(30):
            prediction = model.predict(last_window)
            predictions.append(prediction[0, 0])
            prediction = prediction.reshape(1, 1, 1)
            last_window = np.append(last_window[:, 1:, :], prediction, axis=1)
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = predictions * (np.max(data) - np.min(data)) + np.min(data)
        predicted_prices = [(i + 1, pred[0]) for i, pred in enumerate(predictions)]
        return render_template('result.html', symbol=symbol, predicted_prices=predicted_prices,from_date= end_date)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
