import requests
import random
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
import csv

# Number of requests to send
num_requests = 1000

# URL of the Flask app
url = "http://localhost:8000/"  # Change this if your server is running on a different host or port

# Path to the CSV log file
log_file_path = 'request_log.csv'

# List to store log data
log_data = []
status_counts = {200: 0, 503: 0}

def send_request(request_number):
    try:
        # Generate a unique Request-ID for each request
        request_id = str(uuid.uuid4())
        
        # Example Authorization token (you may replace this with a real token)
        token = f"Bearer token_{request_number}"
        
        # Headers to include in each request
        headers = {
            'Authorization': token,
            'Request-ID': request_id
        }

        # Determine whether to return status 200 or 503 based on the 70:30 ratio
        status_code = random.choices([200, 503], weights=[70, 30], k=1)[0]

        # Simulate the server's response based on the chosen status code
        if status_code == 200:
            response = requests.get(url, headers=headers)
            elapsed_time = response.elapsed.total_seconds()
        else:
            # Simulate a 503 Service Unavailable response
            elapsed_time = random.uniform(0.1, 1.0)  # Simulated response time

        # Log request status and time
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request_number, status_code, elapsed_time])
        
        status_counts[status_code] += 1
        print(f"Request {request_number}: Status Code = {status_code}, Time = {elapsed_time:.2f}s")

    except requests.exceptions.RequestException as e:
        print(f"Request {request_number} failed: {e}")

if __name__ == "__main__":
    # Start sending requests
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(send_request, i + 1) for i in range(num_requests)]
        for future in futures:
            future.result()

    print("200:", status_counts[200])
    print("503:", status_counts[503])
    print("Load test completed.")
