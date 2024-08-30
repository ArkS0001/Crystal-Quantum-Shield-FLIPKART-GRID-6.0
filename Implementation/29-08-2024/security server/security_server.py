from flask import Flask, request, jsonify
import csv
from datetime import datetime

security_app = Flask(__name__)

# CSV log file path for security checks
SECURITY_LOG_FILE = 'security_checks.csv'

# Dummy security check function
def is_request_secure(data):
    username = data.get('username')
    # Placeholder logic for checking API security
    if username:
        return True  # Replace with actual security checks
    return False

def log_security_check(username, secure):
    """Log security check attempts to a CSV file."""
    with open(SECURITY_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), username, "Secure" if secure else "Not Secure"])

@security_app.route('/check_security', methods=['POST'])
def check_security():
    data = request.json
    secure = is_request_secure(data)
    log_security_check(data.get('username'), secure)
    
    if secure:
        return jsonify({'secure': True}), 200
    return jsonify({'secure': False}), 403

if __name__ == '__main__':
    # Create CSV file with headers if not exists
    with open(SECURITY_LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Username', 'Security Status'])
    
    security_app.run(port=5001, debug=True)
