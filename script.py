users = {'admin': 'password'}

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
