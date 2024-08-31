import requests
import time
import threading

# Configuration
url = 'http://localhost/secure'  # Adjust based on your setup
num_requests = 100          # Number of requests to send
interval = 0.1             # Interval between requests in seconds

def send_request():
    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}, Response Text: {response.text}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def main():
    threads = []
    
    # Create and start threads to send requests
    for _ in range(num_requests):
        t = threading.Thread(target=send_request)
        t.start()
        threads.append(t)
        time.sleep(interval)  # Adjust the interval to test different request rates

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
