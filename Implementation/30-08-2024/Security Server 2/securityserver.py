import logging
import csv
from logging import handlers
from flask import Flask, jsonify, request

app = Flask(__name__)

# Custom CSV Logging Handler
class CSVHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        # Create the CSV file and write the header if it doesn't exist
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                writer.writerow(['Timestamp', 'Level', 'Message', 'Action', 'Status', 'Secure'])

    def emit(self, record):
        # Only write logs related to login and logout actions
        if 'Login' in record.getMessage() or 'Logout' in record.getMessage():
            log_entry = [
                self.formatTime(record),
                record.levelname,
                record.getMessage(),
                getattr(record, 'action', 'N/A'),
                getattr(record, 'status', 'N/A'),
                getattr(record, 'secure', 'N/A')
            ]
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(log_entry)

    def formatTime(self, record, datefmt=None):
        return self.formatter.formatTime(record, datefmt)

# Setup CSV logging
csv_handler = CSVHandler('securityserver.csv')
csv_handler.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s,%(message)s'))
logging.getLogger().addHandler(csv_handler)
logging.getLogger().setLevel(logging.INFO)

# Dummy users data
users = {
    'admin': 'password123',
    'user': 'userpass'
}

@app.route('/api/security/login', methods=['POST'])
def login_security():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    action = "login"

    logging.info(f"Login attempt by {username}", extra={'action': action, 'status': 'Attempt', 'secure': 'Yes'})

    if username in users and users[username] == password:
        logging.info(f"Login successful for {username}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
        return jsonify({'message': 'Login successful'}), 200
    else:
        logging.warning(f"Login failed for {username}", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/security/logout', methods=['POST'])
def logout_security():
    data = request.json
    username = data.get('username')
    action = "logout"

    logging.info(f"Logout attempt by {username}", extra={'action': action, 'status': 'Attempt', 'secure': 'Yes'})
    
    # Implement any necessary logout logic here
    logging.info(f"Logout successful for {username}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
