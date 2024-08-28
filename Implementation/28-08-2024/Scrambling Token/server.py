from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
import random
import csv
import os

app = Flask(__name__)

# Generate or load a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Path to the log file
log_file_path = 'request_logs.csv'

# Initialize the CSV file with headers if it doesn't exist
def initialize_csv():
    if not os.path.exists(log_file_path):
        with open(log_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Request_ID', 'Authorization_Token', 'Scrambled_Token'])

initialize_csv()

# Function to scramble the token
def scramble_token(token):
    token_list = list(token)
    random.shuffle(token_list)
    return ''.join(token_list)

# Middleware to scramble the Authorization token and log it
@app.before_request
def scramble_and_log_request():
    token = request.headers.get('Authorization')
    request_id = request.headers.get('Request-ID', 'N/A')  # Optional: Use a custom request ID if available

    if token:
        scrambled_token = scramble_token(token)
        encrypted_token = cipher_suite.encrypt(token.encode()).decode()
        
        # Log the request details
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request_id, encrypted_token, scrambled_token])

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/api/data', methods=['GET'])
def get_data():
    # Check for the Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token is missing'}), 401

    # Example data
    data = {
        'id': 1,
        'name': 'Sample Data',
        'description': 'This is a sample API response.'
    }
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def create_data():
    # Check for the Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token is missing'}), 401

    # Retrieve data from the request
    new_data = request.json
    response = {
        'message': 'Data created successfully',
        'data': new_data
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
