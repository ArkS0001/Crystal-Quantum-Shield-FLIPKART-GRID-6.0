import logging
import csv
from logging import handlers
from flask import Flask, jsonify, request
import oqs
import binascii

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
                writer.writerow(['Timestamp', 'Level', 'Message', 'Action', 'Status', 'Secure', 'Encryption Details'])

    def emit(self, record):
        # Write only relevant log entries (exclude Flask default logs)
        if record.name == "app_logger":
            log_entry = [
                self.formatTime(record),
                record.levelname,
                record.getMessage(),
                getattr(record, 'action', 'N/A'),
                getattr(record, 'status', 'N/A'),
                getattr(record, 'secure', 'N/A'),
                getattr(record, 'encryption_details', 'N/A')
            ]
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(log_entry)

    def formatTime(self, record, datefmt=None):
        return self.formatter.formatTime(record, datefmt)

# Setup a separate logger for app-specific logs
app_logger = logging.getLogger("app_logger")
csv_handler = CSVHandler('securityserver.csv')
csv_handler.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s,%(message)s'))
app_logger.addHandler(csv_handler)
app_logger.setLevel(logging.INFO)


# Dummy users data
users = {
    'email@gmail.com':'xxx'
}

# Kyber key exchange
def perform_key_exchange():
    kemalg = "Kyber1024"
    
    try:
        # Initialize client and server for Kyber key encapsulation
        with oqs.KeyEncapsulation(kemalg) as client:
            with oqs.KeyEncapsulation(kemalg) as server:
                # Client generates its keypair
                public_key_client = client.generate_keypair()
                
                # Server encapsulates its secret using the client's public key
                ciphertext, shared_secret_server = server.encap_secret(public_key_client)
                
                # Client decapsulates the server's ciphertext to obtain the shared secret
                shared_secret_client = client.decap_secret(ciphertext)
                
                return {
                    "client_public_key": public_key_client.hex(),
                    "ciphertext": ciphertext.hex(),
                    "shared_secret_server": shared_secret_server.hex(),
                    "shared_secret_client": shared_secret_client.hex(),
                    "keys_match": shared_secret_client == shared_secret_server,
                }
    
    except Exception as e:
        return {
            "error": str(e)
        }

# Dilithium signing
def sign_message(message):
    sigalg = "Dilithium2"
    with oqs.Signature(sigalg) as signer:
        signer_public_key = signer.generate_keypair()
        signature = signer.sign(message.encode())

        return {
            "signer_public_key": signer_public_key.hex(),
            "signature": signature.hex()
        }

# Dilithium verification
def verify_signature(message, signature, signer_public_key):
    sigalg = "Dilithium2"
    with oqs.Signature(sigalg) as verifier:
        is_valid = verifier.verify(message.encode(), binascii.unhexlify(signature), binascii.unhexlify(signer_public_key))
        return {"is_valid": is_valid}

# Middleware for securing each API call
@app.before_request
def secure_request():
    # Kyber key exchange for securing communication
    kyber_data = perform_key_exchange()
    if 'error' in kyber_data:
        return jsonify({'error': kyber_data['error']}), 500

    # Dilithium signature verification (simulating client signing for now)
    message = request.path
    signature_data = sign_message(message)  # Assume client signed this message
    verification_result = verify_signature(message, signature_data['signature'], signature_data['signer_public_key'])

    encryption_details = f"Keys Match: {kyber_data.get('keys_match')}, Signature Valid: {verification_result['is_valid']}"
    
    if not verification_result['is_valid']:
        app_logger.warning(f"Signature verification failed for request to {request.path}",
                        extra={'action': 'API Call', 'status': 'Failed', 'secure': 'No', 'encryption_details': encryption_details})
        return jsonify({'error': 'Invalid signature'}), 401

    app_logger.info(f"API call to {request.path} secured", 
                 extra={'action': 'API Call', 'status': 'Successful', 'secure': 'Yes', 'encryption_details': encryption_details})


@app.route('/api/security/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    action = "register"

    if not email or not password:
        app_logger.warning(f"Registration failed: Missing email or password", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Missing email or password'}), 400

    if email in users:
        app_logger.warning(f"Registration failed: User {email} already exists", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'User already exists'}), 409

    # Store the new user in the `users` dictionary (consider using a database in production)
    users[email] = password
    app_logger.info(f"User {email} registered successfully", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
    
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/security/login', methods=['POST'])
def login_security():
    data = request.json
    username = data.get('email')
    password = data.get('password')
    action = "login"

    if username in users and users[username] == password:
        app_logger.info(f"Login successful for {username}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
        return jsonify({'message': 'Login successful'}), 200
    else:
        app_logger.warning(f"Login failed for {username}", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/security/logout', methods=['POST'])
def logout_security():
    data = request.json
    username = data.get('email')
    action = "logout"

    app_logger.info(f"Logout successful for {username}", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})
    return jsonify({'message': 'Logout successful'}), 200

# Example of a generic API call
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'Some secure data'}), 200

if __name__ == '__main__':
    # Disable Flask's default logger output to CSV
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(debug=True, port=5001)