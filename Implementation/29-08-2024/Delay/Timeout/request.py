import requests
import time

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
            # Print status and response text
            print(f"Request {i+1}: Status Code: {response.status_code}, Response: {response.json()}")
        except requests.RequestException as e:
            # Print error details
            print(f"Request {i+1} failed: {e}")
        
        # Optional delay between requests
        time.sleep(request_delay)

if __name__ == "__main__":
    send_requests()
