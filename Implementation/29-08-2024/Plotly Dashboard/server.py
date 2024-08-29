from flask import Flask, jsonify, request, Response
from cryptography.fernet import Fernet
from prometheus_client import CollectorRegistry, Gauge, generate_latest, write_to_textfile
import random
import csv
import time

app = Flask(__name__)

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Path to the log file
log_file_path = 'request_logs.csv'

# Initialize the CSV file with headers if it doesn't exist
def initialize_csv():
    with open(log_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Request_ID', 'Authorization_Token', 'Scrambled_Token'])

initialize_csv()

# Function to scramble the token
def scramble_token(token):
    token_list = list(token)
    random.shuffle(token_list)
    return ''.join(token_list)

# Prometheus metrics
registry = CollectorRegistry()
REQUEST_COUNT = Gauge('http_request_total', 'Total number of HTTP requests', ['status_code'], registry=registry)
REQUEST_LATENCY = Gauge('http_request_latency_seconds', 'HTTP request latency', registry=registry)

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
    start_time = time.time()
    
    token = request.headers.get('Authorization')
    if not token:
        REQUEST_COUNT.labels(status_code='401').inc()
        return jsonify({'error': 'Authorization token is missing'}), 401

    data = {
        'id': 1,
        'name': 'Sample Data',
        'description': 'This is a sample API response.'
    }

    latency = time.time() - start_time
    REQUEST_LATENCY.set(latency)
    REQUEST_COUNT.labels(status_code='200').inc()

    return jsonify(data)

@app.route('/metrics')
def metrics():
    # Save the current metrics to a file
    write_to_textfile('metrics.prom', generate_latest(registry))
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
