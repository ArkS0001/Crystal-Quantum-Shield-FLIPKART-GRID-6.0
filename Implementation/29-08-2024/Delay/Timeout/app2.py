# from flask import Flask, request, jsonify
# import logging
# import time
# import threading
# import signal

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

# def timeout_handler(signum, frame):
#     raise TimeoutError

# def run_with_timeout(func, timeout):
#     signal.signal(signal.SIGALRM, timeout_handler)
#     signal.alarm(timeout)  # Set the alarm for the timeout
#     try:
#         result = func()
#     except TimeoutError:
#         return jsonify({'error': 'Request timed out'}), 503
#     finally:
#         signal.alarm(0)  # Disable the alarm
#     return result

# # Endpoint to simulate processing with a timeout
# @app.route('/api/data', methods=['GET'])
# def api_data():
#     def process_request():
#         # Simulate processing delay
#         delay = float(request.args.get('delay', 0))
#         if delay > 0:
#             time.sleep(delay)  # Simulate processing delay
#         return jsonify({'message': 'Hello, user!'})

#     # Run the request with a timeout of 200 milliseconds
#     return run_with_timeout(process_request, timeout=0.2)

# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)


from flask import Flask, request, jsonify
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ThreadPoolExecutor for running tasks with timeout
executor = ThreadPoolExecutor(max_workers=1)

# Function to log incoming requests
@app.before_request
def log_request_info():
    logging.info(f"Request method: {request.method}")
    logging.info(f"Request URL: {request.url}")
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request body: {request.get_data(as_text=True)}")

def process_request():
    # Simulate processing delay
    delay = float(request.args.get('delay', 0))
    if delay > 0:
        time.sleep(delay)  # Simulate processing delay
    return jsonify({'message': 'Hello, user!'})

@app.route('/api/data', methods=['GET'])
def api_data():
    try:
        future = executor.submit(process_request)
        # Wait for 200 milliseconds (0.2 seconds) for the result
        response = future.result(timeout=0.2)
        return response
    except TimeoutError:
        logging.error('Request timed out')
        return jsonify({'error': 'Request timed out'}), 503
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
