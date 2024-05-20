from flask import Flask, render_template

USERS_DETAILS = {'Admin': 'password123'}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stockdashboard.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in USERS_DETAILS and USERS_DETAILS[username] == password:
        print("Account Login successful.")
        return True
    else:
        print("Incorrect credentials. Login unsuccessful.")
        return False

def display_dashboard(stock_price, stock_projection):
    return f"Stock Price: ${stock_price}<br>Projection: ${stock_projection}"

@app.route('/dashboard')
def main():
    print("Welcome to the Stock Prediction System!")

    if login():
        stock_price = 122.50
        stock_projection = 160.00
        dashboard_info = display_dashboard(stock_price, stock_projection)
        return dashboard_info
    else:
        return "Login unsuccessful. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ticker = request.form["ticker"]
        stock_data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        stock_data['Close'] = stock_data['Close'].fillna(method='ffill')
        ts_data = stock_data['Close'].values.reshape(-1, 1)
        ts_data_normalized = scaler.fit_transform(ts_data)