# from flask import Flask, request, jsonify
# import logging
# import time
# from threading import Thread

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(
#     filename='app.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # Function to log incoming requests
# @app.before_request
# def log_request_info():
#     logging.info(f"Request method: {request.method}")
#     logging.info(f"Request URL: {request.url}")
#     logging.info(f"Request headers: {request.headers}")
#     logging.info(f"Request body: {request.get_data(as_text=True)}")

# # Endpoint to simulate processing with timeout
# @app.route('/api/data', methods=['GET'])
# def api_data():
#     try:
#         # Simulate processing delay
#         delay = float(request.args.get('delay', 0))
#         if delay > 0:
#             time.sleep(delay)  # Simulate processing delay

#         return jsonify({'message': 'Hello, user!'})
#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         return jsonify({'error': 'Internal Server Error'}), 500

# # Function to run Flask with a timeout feature
# def run_flask_app():
#     from werkzeug.serving import run_simple
#     run_simple('127.0.0.1', 5000, app, threaded=True)

# if __name__ == "__main__":
#     # Run the Flask app in a separate thread to manage timeout
#     thread = Thread(target=run_flask_app)
#     thread.start()

#     # Wait for the thread to finish
#     thread.join()
from flask import Flask, request, jsonify
import logging
import time
from threading import Thread

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to log incoming requests
@app.before_request
def log_request_info():
    logging.info(f"Request method: {request.method}")
    logging.info(f"Request URL: {request.url}")
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request body: {request.get_data(as_text=True)}")

# Endpoint to simulate processing with timeout
@app.route('/api/data', methods=['GET'])
def api_data():
    try:
        # Simulate processing delay
        delay = float(request.args.get('delay', 0))
        if delay > 0:
            time.sleep(delay)  # Simulate processing delay

        return jsonify({'message': 'Hello, user!'})
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Function to run Flask with a timeout feature
def run_flask_app():
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, threaded=True)

if __name__ == "__main__":
    # Run the Flask app in a separate thread to manage timeout
    thread = Thread(target=run_flask_app)
    thread.start()

    # Wait for the thread to finish
    thread.join()
