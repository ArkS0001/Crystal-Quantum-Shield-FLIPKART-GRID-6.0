import requests

# # GET request with Authorization header
# url = "http://localhost/api/data"
# headers = {
#     "Authorization": "Bearer exampletoken123"
# }

# response = requests.get(url, headers=headers)
# print(response.json())

# # POST request with Authorization header
# url = "http://localhost/api/data"
# headers = {
#     "Authorization": "Bearer exampletoken123",
#     "Content-Type": "application/json"
# }
# data = {
#     "key": "value"
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.json())

# Function to send a single request
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import uuid

# Number of requests to send
num_requests = 1000

# URL of the NGINX server
url = "http://localhost:8000/api/data"  # Ensure this matches your Flask server's endpoint

# Function to send a single request
def send_request(request_number):
    # Generate a unique Request-ID for each request
    request_id = str(uuid.uuid4())
    
    # Example Authorization token (you may replace this with a real token)
    token = f"Bearer token_{request_number}"
    
    # Headers to include in each request
    headers = {
        'Authorization': token,
        'Request-ID': request_id
    }

    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        elapsed_time = response.elapsed.total_seconds()
        
        print(f"Request {request_number}: Status Code = {status_code}, Time = {elapsed_time}s")
    except requests.exceptions.RequestException as e:
        print(f"Request {request_number} failed: {e}")

# Using ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(send_request, i + 1) for i in range(num_requests)]

# Optional: Wait for all requests to complete
for future in futures:
    future.result()

print("Load test completed.")
