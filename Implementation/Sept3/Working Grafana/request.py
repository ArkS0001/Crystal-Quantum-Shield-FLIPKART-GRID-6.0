import requests
import time
import threading
import csv
import random

# Configuration
url_login = 'http://localhost/api/security/login'
url_register = 'http://localhost/api/security/register'
num_requests = 1000
interval = 0.01
csv_file = 'log.csv'

# Initialize CSV file
def init_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Request Number', 'Type', 'Status Code', 'Success'])

# Log request details to CSV
def log_to_csv(request_number, request_type, status_code, success):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request_number, request_type, status_code, success])

# Function to send login request
def send_login_request(request_number):
    login_data_list = [
        {"email": "email@gmail.com", "password": "xxx"},
        {'email':'admin1@example.com','password': 'adminpass1'},
        {"email": "admin2@example.com", "password": "adminpass2"},
        {"email": "wrongemail@gmail.com", "password": "wrongpassword"}
    ]
    data = random.choice(login_data_list)
    try:
        response = requests.post(url_login, json=data)
        status_code = response.status_code
        success = 'Yes' if status_code == 200 else 'No'
        log_to_csv(request_number, 'Login', status_code, success)
        print(f"Request {request_number} (Login): Status Code: {status_code}, Success: {success}")
    except requests.RequestException as e:
        print(f"Request {request_number} (Login) failed: {e}")

# Function to send registration request
def send_registration_request(request_number):
    register_data_list = [
        {
            "email": "newuser1@example.com", 
            "password": "userpass1"
        },
        {
            "email": "newuser2@example.com", 
            "password": "userpass2"
        },
        {
            "email": "email@gmail.com", 
            "password": "userpass3"
        },
        {
            "email": "invaliduser@example.com",  # Invalid registration data
            "password": "sh"  # Too short password, or other invalid data
        }
    ]
    data = random.choice(register_data_list)
    try:
        response = requests.post(url_register, json=data)
        status_code = response.status_code
        success = 'Yes' if status_code == 200 else 'No'
        log_to_csv(request_number, 'Register', status_code, success)
        print(f"Request {request_number} (Register): Status Code: {status_code}, Success: {success}")
    except requests.RequestException as e:
        print(f"Request {request_number} (Register) failed: {e}")

def main():
    init_csv()  # Initialize the CSV file
    threads = []

    # Create and start threads to send requests
    for i in range(1, num_requests + 1):
        if i % 2 == 0:
            t = threading.Thread(target=send_login_request, args=(i,))
        else:
            t = threading.Thread(target=send_registration_request, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(interval)

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
