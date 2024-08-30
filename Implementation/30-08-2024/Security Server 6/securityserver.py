import logging
import csv
import jwt  # Import JWT library
from datetime import datetime, timedelta
from logging import handlers
from flask import Flask, jsonify, request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for JWT encoding/decoding

# Custom CSV Logging Handler
class CSVHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Timestamp', 'Level', 'Message', 'Action', 'Status', 'Secure', 'Encryption Details', 'Scrambled Token'])

    def emit(self, record):
        if record.name == "app_logger":
            log_entry = [
                self.formatTime(record),
                record.levelname,
                record.getMessage(),
                getattr(record, 'action', 'N/A'),
                getattr(record, 'status', 'N/A'),
                getattr(record, 'secure', 'N/A'),
                getattr(record, 'encryption_details', 'N/A'),
                getattr(record, 'scrambled_token', 'N/A')
            ]
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(log_entry)

    def formatTime(self, record, datefmt=None):
        return self.formatter.formatTime(record, datefmt)

app_logger = logging.getLogger("app_logger")
csv_handler = CSVHandler('securityserver.csv')
csv_handler.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s,%(message)s'))
app_logger.addHandler(csv_handler)
app_logger.setLevel(logging.INFO)

# Dummy users data
users = {
    'email@gmail.com': 'xxx'
}

# Function to generate JWT
def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Function to decode and verify JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Function to scramble the token
def scramble_token(token):
    token_list = list(token)
    random.shuffle(token_list)
    return ''.join(token_list)

@app.route('/api/security/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    action = "register"

    if not email or not password:
        app_logger.warning(f"Registration failed: Missing email or password", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Missing email or password'}), 400

    if email in users:
        app_logger.warning(f"Registration failed: User {email} already exists", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'User already exists'}), 409

    # Store the new user in the `users` dictionary
    users[email] = password
    token = generate_jwt(email)  # Generate JWT
    scrambled_token = scramble_token(token)  # Scramble the JWT

    # Log registration
    app_logger.info(f"User {email} registered successfully", extra={'action': action, 'status': 'Successful', 'secure': 'Yes', 'scrambled_token': scrambled_token})

    return jsonify({'message': 'Registration successful', 'token': token}), 201

@app.route('/api/security/login', methods=['POST'])
def login_security():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    action = "login"

    if not email or not password:
        app_logger.warning(f"Login failed: Missing email or password", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Missing email or password'}), 400

    if email in users and users[email] == password:
        token = generate_jwt(email)  # Generate JWT
        scrambled_token = scramble_token(token)  # Scramble the JWT

        # Log login
        app_logger.info(f"Login successful for {email}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes', 'scrambled_token': scrambled_token})

        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        app_logger.warning(f"Login failed for {email}", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/security/logout', methods=['POST'])
def logout_security():
    data = request.json
    email = data.get('email')
    action = "logout"

    app_logger.info(f"Logout successful for {email}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        payload = verify_jwt(token)
        if payload:
            return jsonify({'data': 'Some secure data'}), 200
        else:
            return jsonify({'message': 'Invalid or expired token'}), 401
    else:
        return jsonify({'message': 'Missing token'}), 400

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(debug=True, port=5001)
