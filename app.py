from flask import Flask, render_template, request
import numpy as np
import yfinance as yf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import shap

app = Flask(__name__)

# Function to create a sliding window of data
def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:(i + window_size), 0])
        y.append(data[i + window_size, 0])
    return np.array(X), np.array(y)

def save_plot_stock_trend(var, cur_title, stockprices):
    ax = stockprices[["Close", var, "200day"]].plot(figsize=(20, 10))
    plt.grid(False)
    plt.title(cur_title)
    plt.axis("tight")
    plt.ylabel("Stock Price ($)")
    plt.savefig(f"static/{var}.png")

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def predict_stock():
    if request.method == 'POST':
        symbol = request.form['symbol']
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=1000)).strftime('%Y-%m-%d')
        stockprice = yf.download(symbol, start=start_date, end=end_date)
        if stockprice.empty:
            return render_template('index.html', error = "Invalid Symbol")
        stock = yf.Ticker(symbol)
        news = stock.news
        data = stockprice['Close'].values.reshape(-1, 1)
        print(stockprice.head())
        window_size = 30
        window_var = f"{window_size}day"
        stockprice[window_var] = stockprice["Close"].rolling(window_size).mean()
        stockprice["60days"] = stockprice["Close"].rolling(60).mean()
        stockprice["200day"] = stockprice["Close"].rolling(200).mean()

        save_plot_stock_trend(var=window_var, cur_title="Simple Moving Averages", stockprices=stockprice)

        data_normalized = (data - np.min(data)) / (np.max(data) - np.min(data))
        
        X, y = create_dataset(data_normalized, window_size)
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(window_size, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X.reshape(X.shape[0], X.shape[1], 1), y, epochs=10, batch_size=32)
        last_window = data_normalized[-window_size:].reshape(1, window_size, 1)
        predictions = []
        for _ in range(30):
            prediction = model.predict(last_window)
            predictions.append(prediction[0, 0])
            prediction = prediction.reshape(1, 1, 1)
            last_window = np.append(last_window[:, 1:, :], prediction, axis=1)
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = predictions * (np.max(data) - np.min(data)) + np.min(data)
        d = data[-1][0] - predictions[0][0]
        print(d, data[-1][0], predictions[0][0])
        predicted_prices = [(i + 1, pred[0] + d) for i, pred in enumerate(predictions)]
        # Print model metrics
        loss = model.evaluate(X, y)
        print("Loss:", loss)

        # Calculate additional performance measures
        predictions_normalized = (predictions - np.min(data)) / (np.max(data) - np.min(data))
        actual_values = data[-len(predictions):]
        actual_values_normalized = (actual_values - np.min(data)) / (np.max(data) - np.min(data))

        # Calculate mean absolute error (MAE)
        mae = np.mean(np.abs(predictions_normalized - actual_values_normalized))
        print("MAE:", mae)

        # Calculate root mean squared error (RMSE)
        rmse = np.sqrt(np.mean(np.square(predictions_normalized - actual_values_normalized)))
        print("RMSE:", rmse)

        # Calculate mean absolute percentage error (MAPE)
        mape = np.mean(np.abs((predictions_normalized - actual_values_normalized) / actual_values_normalized)) * 100
        print("MAPE:", mape)

        # Create a table of performance measures
        performance_table = {
            "Loss": loss,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        }
        print("\nPerformance Measures:")
        print(performance_table)

        # # Generate SHAP values
        # explainer = shap.Explainer(model, X)
        # shap_values = explainer.shap_values(X)

        # # Plot SHAP summary plot
        # shap.summary_plot(shap_values, X, show=False)
        # plt.savefig("static/shap_summary_plot_main.png")

        return render_template('result.html', symbol=symbol, predicted_prices=predicted_prices, from_date=end_date, news=news, metrics=performance_table, shap_summary_plot="static/shap_summary_plot.png", shap_dependence_plot="static/shap_dependence_plot.png")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
