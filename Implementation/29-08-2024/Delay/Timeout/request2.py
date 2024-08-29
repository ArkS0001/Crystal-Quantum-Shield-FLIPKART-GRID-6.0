import requests
import time
import logging

# Configure logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL of the Flask API
url = "http://localhost:5000/api/data"

# Number of requests to send
num_requests = 200

# Optional delay between requests (in seconds)
request_delay = 0.1  # Adjust as needed

def send_requests():
    for i in range(num_requests):
        try:
            # Send GET request
            response = requests.get(url, params={'delay': 0})  # You can adjust the delay parameter if needed
            
            # Log status and response text
            log_message = f"Request {i+1}: Status Code: {response.status_code}, Response: {response.json()}"
            logging.info(log_message)
            print(log_message)
        except requests.RequestException as e:
            # Log error details
            error_message = f"Request {i+1} failed: {e}"
            logging.error(error_message)
            print(error_message)
        
        # Optional delay between requests
        time.sleep(request_delay)

if __name__ == "__main__":
    send_requests()
