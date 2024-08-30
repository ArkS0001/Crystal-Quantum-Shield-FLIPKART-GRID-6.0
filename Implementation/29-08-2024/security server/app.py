from flask import Flask, render_template, request, redirect, url_for, session
import requests
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a real key for session management

# Dummy user database
users = {
    "user1": "password1",
    "user2": "password2"
}

# URL for the security server
SECURITY_SERVER_URL = 'http://127.0.0.1:5001/check_security'

# CSV log file path
LOG_FILE = 'login_attempts.csv'

def log_to_csv(username, status):
    """Log login attempts to a CSV file."""
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), username, status])

@app.route('/')
def home():
    if 'username' in session:
        return f"Hello {session['username']}! You are logged in."
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username in users and users[username] == password:
            # Now check API security using the security server
            security_response = requests.post(SECURITY_SERVER_URL, json={'username': username})
            if security_response.status_code == 200 and security_response.json().get('secure'):
                session['username'] = username
                log_to_csv(username, "Login successful")
                return redirect(url_for('home'))
            else:
                log_to_csv(username, "Blocked by security check")
                return "Login blocked by security check."
        else:
            log_to_csv(username, "Invalid credentials")
            return "Invalid credentials, please try again!"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Create CSV file with headers if not exists
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Username', 'Status'])
    
    app.run(port=5000, debug=True)
