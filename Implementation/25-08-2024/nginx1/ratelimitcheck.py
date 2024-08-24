import requests
import time

# Number of requests to send
num_requests = 30

# URL of the NGINX server (Change this if needed)
url = "http://localhost/"

# Send multiple requests
for i in range(num_requests):
    response = requests.get(url)
    
    # Print the status code and response time for each request
    print(f"Request {i+1}: Status Code = {response.status_code}, Time = {response.elapsed.total_seconds()}s")
    
    # Small delay between requests (tweak this to test different scenarios)
    time.sleep(0.1)
