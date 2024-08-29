from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# Secret key for encoding and decoding JWT tokens
app.config['SECRET_KEY'] = 'your_secret_key'

# Function to create a new JWT token
def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Endpoint to generate a JWT token (for testing)
@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    token = create_token(user_id)
    return jsonify({'token': token})

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
