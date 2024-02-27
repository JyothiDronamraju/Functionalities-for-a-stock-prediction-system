from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define user credentials
users = {'admin': 'password'}

@app.route('/')
def index():
    return render_template('stockdashboard.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        # Redirect to homepage if login is successful
        return redirect(url_for('homepage'))
    else:
        # Redirect back to the login page with a message
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
