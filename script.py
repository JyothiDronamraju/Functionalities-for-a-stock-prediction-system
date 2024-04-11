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
