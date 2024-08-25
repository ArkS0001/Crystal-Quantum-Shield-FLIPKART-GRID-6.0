import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Number of requests to send
num_requests = 1000

# URL of the NGINX server
url = "http://localhost/"  # Change this if your server is running on a different host or port

# Function to send a single request
def send_request(request_number):
    try:
        response = requests.get(url)
        print(f"Request {request_number}: Status Code = {response.status_code}, Time = {response.elapsed.total_seconds()}s")
    except requests.exceptions.RequestException as e:
        print(f"Request {request_number} failed: {e}")

# Using ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(send_request, i + 1) for i in range(num_requests)]

# Optional: Wait for all requests to complete
for future in futures:
    future.result()

print("Load test completed.")