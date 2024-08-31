import requests
import time
import threading
import csv

# Configuration
url = 'http://localhost/secure'  # Adjust based on your setup
num_requests = 1000          # Number of requests to send
interval = 0.01             # Interval between requests in seconds
csv_file = 'response_log.csv' # Output CSV file

def send_request(results):
    try:
        response = requests.get(url)
        # Append the result to the list
        results.append((response.status_code, response.text))
    except requests.RequestException as e:
        # Append the error to the list
        results.append(('Error', str(e)))

def main():
    threads = []
    results = []

    # Create and start threads to send requests
    for _ in range(num_requests):
        t = threading.Thread(target=send_request, args=(results,))
        t.start()
        threads.append(t)
        time.sleep(interval)  # Adjust the interval to test different request rates

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Write results to CSV
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Status Code', 'Response Text'])  # Header row
        writer.writerows(results)  # Data rows

if __name__ == "__main__":
    main()
