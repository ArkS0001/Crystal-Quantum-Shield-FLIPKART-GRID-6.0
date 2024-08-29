from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# Secret key for encoding and decoding JWT tokens
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['REFRESH_SECRET_KEY'] = 'your_refresh_secret_key'

# Function to create a new JWT token
def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),  # Short-lived access token
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Function to create a new refresh token
def create_refresh_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Longer-lived refresh token
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['REFRESH_SECRET_KEY'], algorithm='HS256')

# Endpoint to generate a JWT token and refresh token (for testing)
@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    token = create_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return jsonify({'token': token, 'refresh_token': refresh_token})

# Endpoint to refresh JWT token
@app.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.json
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing!'}), 403

    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, app.config['REFRESH_SECRET_KEY'], algorithms=['HS256'])
        # Generate a new access token
        new_token = create_token(payload['sub'])
        return jsonify({'token': new_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token!'}), 403

# Endpoint that requires JWT token
@app.route('/api/data', methods=['GET'])
def api_data():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403

    try:
        # Extract the token from the 'Bearer ' prefix
        token = token.split(' ')[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 403

    return jsonify({'message': 'Hello, user!'})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
