from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SECURITY_SERVER_URL = 'http://localhost:5001'

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/api/data', methods=['GET'])
def get_data():
    # Request to security server for security
    response = requests.get(f'{SECURITY_SERVER_URL}/secure', headers={'Authorization': 'Bearer YOUR_ACCESS_TOKEN'})
    if response.status_code == 200:
        data = {
            'id': 1,
            'name': 'Sample Data',
            'description': 'This is a sample API response.'
        }
        return jsonify(data)
    else:
        return jsonify({'message': 'Security check failed'}), 403

@app.route('/api/data', methods=['POST'])
def create_data():
    # Retrieve data from the request
    new_data = request.json
    # Request to security server for security
    response = requests.post(f'{SECURITY_SERVER_URL}/secure', json=new_data, headers={'Authorization': 'Bearer YOUR_ACCESS_TOKEN'})
    if response.status_code == 200:
        return jsonify({'message': 'Data created successfully', 'data': new_data}), 201
    else:
        return jsonify({'message': 'Security check failed'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
