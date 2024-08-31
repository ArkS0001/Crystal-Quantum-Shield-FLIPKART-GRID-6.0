import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor

# Number of requests to send
num_requests = 1000

# URL of the NGINX server
url = "http://localhost/"  # Change this if your server is running on a different host or port

# List to store log data
log_data = []
d={200:0,503:0}
# Function to send a single request
def send_request(request_number):
    try:
        response = requests.get(url)
        status_code = response.status_code
        elapsed_time = response.elapsed.total_seconds()
        log_data.append([request_number, status_code, elapsed_time])
        if status_code==200:
            d[200]+=1
        if status_code==503:
            d[503]+=1
        print(f"Request {request_number}: Status Code = {status_code}, Time = {elapsed_time}s")
    except requests.exceptions.RequestException as e:
        log_data.append([request_number, "Failed", str(e)])
        print(f"Request {request_number} failed: {e}")
    
# Using ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(send_request, i + 1) for i in range(num_requests)]

# Optional: Wait for all requests to complete
for future in futures:
    future.result()

# Write log data to a CSV file
with open("load_test_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Request Number", "Status Code", "Elapsed Time (s)"])
    writer.writerows(log_data)

print("Status code 200:",d[200])
print("Status code 503:",d[503])
print("Load test completed. Log saved to load_test_log.csv.")
