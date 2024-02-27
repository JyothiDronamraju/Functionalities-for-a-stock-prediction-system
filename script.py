users = {'admin': 'password'}
from flask import Flask, render_template, send_from_directory

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('stockdashboard.html')
    @app.route('/homepage')
def homepage():
    return render_template('homepage.html')

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username] == password:
        print("Login successful.")
        return True
    else:
        print("Incorrect credentials. Login failed.")
        return False

def display_dashboard(stock_price, stock_projection):
    print("\nStock Dashboard:")
    print(f"Stock Price: ${stock_price}")
    print(f"Projection: ${stock_projection}\n")

def main():
    print("Welcome to the Stock Prediction System!")

    while not login():
        pass

    stock_price = 120.50
    stock_projection = 130.00

    display_dashboard(stock_price, stock_projection)

if __name__ == '__main__':
    main()
    