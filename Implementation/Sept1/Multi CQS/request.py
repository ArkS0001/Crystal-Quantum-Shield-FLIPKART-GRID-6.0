# import asyncio
# import random
# import aiohttp
# import time

# # Number of requests per second
# requests_per_second = 100

# # Total duration in seconds
# duration = 10  # Adjust duration to match the desired number of total requests

# # Calculate total requests
# total_requests = requests_per_second * duration

# # Success and failure counters
# success_count = 0
# fail_count = 0

# # URL to send requests
# url = 'http://localhost:5001/api/security/login'

# # List of valid user data
# user_data_list = [
#     {"email": "email@gmail.com", "password": "xxx"},  # Replace with correct details
#     {'email':'admin1@example.com','password': 'adminpass1'},  # Replace with correct details
#     {"email": "admin2@example.com", "password": "adminpass2"},  # Replace with correct details
#     {
#     "email": "wrongemail@gmail.com",  
#     "password": "wrongpassword"       
# }

#      # Replace with correct details
# ]

# async def fetch(session, data, attempt_label):
#     global success_count, fail_count
#     try:
#         async with session.post(url, json=data) as response:
#             status_code = response.status
#             if status_code == 200:
#                 success_count += 1
#             else:
#                 fail_count += 1
#             proxy_jump = response.headers.get('X-Proxy-Jump', 'None')
#             print(f"{attempt_label} - Status Code = {status_code}, Proxy Jump = {proxy_jump}")
#     except aiohttp.ClientError as e:
#         fail_count += 1
#         print(f"{attempt_label} - Request failed: {e}")

# async def run_requests():
#     # Create a session
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for i in range(total_requests):
#             data = random.choice(user_data_list)  # Randomly select a valid user
#             task = asyncio.ensure_future(fetch(session, data, f"Attempt {i+1}"))
            
#             tasks.append(task)
#             if len(tasks) >= requests_per_second:
#                 # Wait for tasks to complete every second
#                 await asyncio.gather(*tasks)
#                 tasks = []
#                 await asyncio.sleep(1)

# async def main():
#     start_time = time.time()
#     await run_requests()
#     end_time = time.time()
#     print(f"Total Requests: {total_requests}")
#     print(f"Successful Requests (Status 200): {success_count}")
#     print(f"Failed Requests: {fail_count}")
#     print(f"Duration: {end_time - start_time} seconds")

# # Run the main function
# if __name__ == '__main__':
#     asyncio.run(main())



# import requests
# import time
# import threading

# # Configuration
# base_url = 'http://localhost:5001'  # Base URL of the Flask server
# endpoint = '/api/security/login'     # Endpoint to test
# num_requests_per_second = 50         # Number of requests per second
# interval = 1 / num_requests_per_second  # Interval between requests in seconds
# login_data = {
#     'email': 'email@gmail.com',       # Replace with your test email
#     'password': 'xxx'                 # Replace with your test password
# }

# def send_request():
#     try:
#         response = requests.post(base_url + endpoint, json=login_data)
#         print(f"Response Status Code: {response.status_code}, Response Text: {response.text}")
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")

# def main():
#     threads = []
    
#     # Create and start threads to send requests
#     for _ in range(num_requests_per_second):
#         t = threading.Thread(target=send_request)
#         t.start()
#         threads.append(t)
#         time.sleep(interval)  # Adjust the interval to test different request rates

#     # Wait for all threads to complete
#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     main()


# import requests
# import time

# # Configuration
# base_url = 'http://localhost'  # Base URL of the NGINX server
# endpoint = '/api/security/login'   # Endpoint to test
# num_requests = 50                 # Number of requests to send
# interval = 0.1                    # Interval between requests in seconds
# login_data = {
#     'email': 'email@gmail.com',   # Replace with your test email
#     'password': 'xxx'             # Replace with your test password
# }

# def send_request():
#     try:
#         response = requests.post(base_url + endpoint, json=login_data)
#         print(f"Response Status Code: {response.status_code}, Response Text: {response.text}")
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")

# def main():
#     # Create and start threads to send requests
#     for _ in range(num_requests):
#         send_request()
#         time.sleep(interval)  # Adjust the interval to test different request rates

# if __name__ == "__main__":
#     main()

# import requests
# import time

# def test_login_rate_limit(url, email, password, max_requests, interval):
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer YOUR_JWT_TOKEN'  # Replace with a valid JWT token if required
#     }

#     for i in range(max_requests):
#         response = requests.post(url, json={'email': email, 'password': password}, headers=headers)
#         print(f"Request {i+1}: Status Code {response.status_code}")
#         if response.status_code == 429:  # Rate limit exceeded
#             print("Rate limit exceeded. Stopping test.")
#             break
#         elif response.status_code == 200:
#             print("Login successful.")
#         else:
#             print(f"Unexpected response: {response.json()}")
#         time.sleep(interval)

# if __name__ == "__main__":
#     api_url = 'http://localhost:5001/api/security/login'  # URL of the login endpoint
#     test_login_rate_limit(api_url, email='email@gmail.com', password='xxx', max_requests=50, interval=0.5)



# import requests
# import time
# import threading

# # Configuration
# url = 'http://localhost/secure'  # Adjust based on your setup
# num_requests = 100          # Number of requests to send
# interval = 0.1             # Interval between requests in seconds

# def send_request():
#     try:
#         response = requests.get(url)
#         print(f"Response Status Code: {response.status_code}, Response Text: {response.text}")
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")

# def main():
#     threads = []
    
#     # Create and start threads to send requests
#     for _ in range(num_requests):
#         t = threading.Thread(target=send_request)
#         t.start()
#         threads.append(t)
#         time.sleep(interval)  # Adjust the interval to test different request rates

#     # Wait for all threads to complete
#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     main()


import requests
import time
import threading
import csv

# Configuration
url = 'http://localhost/secure'  # Adjust based on your setup
num_requests = 1000              # Number of requests to send
interval = 0.01                 # Interval between requests in seconds
csv_file = 'request_log.csv'   # CSV file to log request details

# Initialize CSV file
def init_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Request Number', 'Status Code', 'Rate Limit Exceeded'])

# Log request details to CSV
def log_to_csv(request_number, status_code, exceeded):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request_number, status_code, exceeded])

def send_request(request_number):
    try:
        response = requests.get(url)
        status_code = response.status_code
        exceeded = 'No' if status_code != 503 else 'Yes'
        log_to_csv(request_number, status_code, exceeded)
        proxy_jump = response.headers.get('X-Proxy-Jump', 'None')
        print(f"Status Code = {status_code}, Proxy Jump = {proxy_jump}")
        print(f"Request {request_number}: Status Code: {status_code}, Rate Limit Exceeded: {exceeded}")
    except requests.RequestException as e:
        print(f"Request {request_number} failed: {e}")

def main():
    init_csv()  # Initialize the CSV file
    threads = []

    # Create and start threads to send requests
    for i in range(1, num_requests + 1):
        t = threading.Thread(target=send_request, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(interval)  # Adjust the interval to test different request rates

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Count occurrences of status codes 200 and 503
    count_200 = 0
    count_503 = 0
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            status_code = int(row[1])
            if status_code == 200:
                count_200 += 1
            elif status_code == 503:
                count_503 += 1

    print(f"Count of Status 200: {count_200}")
    print(f"Count of Status 503: {count_503}")

if __name__ == "__main__":
    main()
