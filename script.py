USERSDETAILS = {'Admin': 'password123'}
from flask import Flask, render_template, send_from_directory

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

    if username in USERSDETAILS and USERSDETAILS[username] == password:
        print("Account Login successful.")
        return True
    else:
        print("Incorrect credentials. Login unsuccessful.")
        return False

def display_dashboard(stock_price, stock_projection):
    print("\nStock Dashboard:")
    print(f"Stock Price: ${stock_price}")
    print(f"Projection: ${stock_projection}\n")

def main():
    print("Welcome to the Stock Prediction System!")

    while not login():
        pass

    stock_price = 122.50
    stock_projection = 160.00

    display_dashboard(stock_price, stock_projection)

if __name__ == '__main__':
    app.run(debug=True)
    main()
