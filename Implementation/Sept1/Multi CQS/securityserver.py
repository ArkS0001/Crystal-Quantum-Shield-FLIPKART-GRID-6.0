import logging
import csv
import jwt
import random
import oqs
import binascii
from datetime import datetime, timedelta
from logging import handlers
from flask import Flask, jsonify, request, redirect, session, url_for
from authlib.integrations.flask_client import OAuth
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Separate secret key for JWT
app.config['SESSION_COOKIE_NAME'] = 'your_session'

# Initialize OAuth
oauth = OAuth(app)

# Register OAuth2 provider (example with Google)
oauth.register(
    name='google',
    client_id='your_google_client_id',
    client_secret='your_google_client_secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5001/auth/callback',
    client_kwargs={'scope': 'openid email profile'},
)


# Custom CSV Logging Handler
class CSVHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Timestamp', 'Level', 'Message', 'Action', 'Status', 'Secure', 'Encryption Details', 'Scrambled Token'])

    def emit(self, record):
        if record.name == "app_logger":
            log_entry = [
                self.formatTime(record),
                record.levelname,
                record.getMessage(),
                getattr(record, 'action', 'N/A'),
                getattr(record, 'status', 'N/A'),
                getattr(record, 'secure', 'N/A'),
                getattr(record, 'encryption_details', 'N/A'),
                getattr(record, 'scrambled_token', 'N/A')
            ]
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(log_entry)

    def formatTime(self, record, datefmt=None):
        return self.formatter.formatTime(record, datefmt)

app_logger = logging.getLogger("app_logger")
csv_handler = CSVHandler('securityserver.csv')
csv_handler.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s,%(message)s'))
app_logger.addHandler(csv_handler)
app_logger.setLevel(logging.INFO)

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Dummy users data
users = {
    'email@gmail.com': 'xxx',
    'admin1@example.com': 'adminpass1',
    'admin2@example.com': 'adminpass2',
    'admin3@example.com': 'adminpass3',
    'admin4@example.com': 'adminpass4',
    'admin5@example.com': 'adminpass5'
}


# Function to generate JWT
def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

# Function to decode and verify JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

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
    sigalg = "Dilithium5"
    with oqs.Signature(sigalg) as signer:
        signer_public_key = signer.generate_keypair()
        signature = signer.sign(message.encode())

        return {
            "signer_public_key": signer_public_key.hex(),
            "signature": signature.hex()
        }

# Dilithium verification
def verify_signature(message, signature, signer_public_key):
    sigalg = "Dilithium5"
    with oqs.Signature(sigalg) as verifier:
        is_valid = verifier.verify(message.encode(), binascii.unhexlify(signature), binascii.unhexlify(signer_public_key))
        return {"is_valid": is_valid}

# Function to scramble the token
def scramble_token(token):
    token_bytes = token.encode('utf-8')
    encrypted_token = cipher_suite.encrypt(token_bytes)
    return encrypted_token.decode('utf-8')

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

    token = request.headers.get('Authorization', '')
    scrambled_token = scramble_token(token)

    if not verification_result['is_valid']:
        app_logger.warning(f"Signature verification failed for request to {request.path}",
                        extra={'action': 'API Call', 'status': 'Failed', 'secure': 'No', 'encryption_details': encryption_details, 'scrambled_token': scrambled_token})
        return jsonify({'error': 'Invalid signature'}), 401

    app_logger.info(f"API call to {request.path} secured",
                 extra={'action': 'API Call', 'status': 'Successful', 'secure': 'Yes', 'encryption_details': encryption_details, 'scrambled_token': scrambled_token})

@app.route('/secure', methods=['GET', 'POST'])
def secure():
    if request.method == 'POST':
        # Log the request data
        data = request.json
        app.logger.info(f"Received POST request with data: {data}")
        return jsonify({'message': 'Data received', 'data': data}), 200
    elif request.method == 'GET':
        # Respond with a simple message
        app.logger.info("Received GET request")
        return jsonify({'message': 'Security server check passed'}), 200

@app.route('/auth/login')
def login_oauth():
    redirect_uri = url_for('auth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)

    if user_info:
        email = user_info['email']
        session['email'] = email
        jwt_token = generate_jwt(email)
        scrambled_token = scramble_token(jwt_token)

        # Log OAuth2 login
        app_logger.info(f"OAuth2 login successful for {email}", extra={'action': 'OAuth2 Login', 'status': 'Successful', 'secure': 'Yes', 'scrambled_token': scrambled_token})

        return jsonify({'message': 'OAuth2 login successful', 'token': jwt_token}), 200
    else:
        app_logger.warning("OAuth2 login failed", extra={'action': 'OAuth2 Login', 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'OAuth2 login failed'}), 401

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

    users[email] = password
    app_logger.info(f"User {email} registered successfully", extra={'action': action, 'status': 'Successful', 'secure': 'Yes'})

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/security/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    action = "login"

    if not email or not password:
        app_logger.warning(f"Login failed: Missing email or password", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Missing email or password'}), 400

    if email not in users or users[email] != password:
        app_logger.warning(f"Login failed: Invalid credentials for {email}", extra={'action': action, 'status': 'Failed', 'secure': 'No'})
        return jsonify({'message': 'Invalid credentials'}), 401

    jwt_token = generate_jwt(email)
    scrambled_token = scramble_token(jwt_token)

    app_logger.info(f"User {email} logged in successfully", extra={'action': action, 'status': 'Successful', 'secure': 'Yes', 'scrambled_token': scrambled_token})

    return jsonify({'message': 'Login successful', 'token': jwt_token}), 200

@app.route('/api/security/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
