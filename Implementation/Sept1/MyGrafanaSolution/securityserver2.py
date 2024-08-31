from flask import Flask, jsonify, request
from prometheus_client import start_http_server, Gauge
import time

app = Flask(__name__)

# Metrics
REQUESTS_TOTAL = Gauge('requests_total', 'Total number of requests received')

@app.route('/secure', methods=['GET', 'POST'])
def secure():
    REQUESTS_TOTAL.inc()  # Increment the total request count
    if request.method == 'POST':
        # Handle POST request
        return jsonify({'message': 'Data received and decrypted'}), 200
    elif request.method == 'GET':
        # Handle GET request
        return jsonify({'message': 'Security server check passed'}), 200

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(8002)  # Expose metrics on port 8002

    # Run Flask application
    app.run(host='0.0.0.0', port=5001)
