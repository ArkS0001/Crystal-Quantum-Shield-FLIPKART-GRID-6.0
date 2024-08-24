from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/api/data', methods=['GET'])
def get_data():
    # Example data
    data = {
        'id': 1,
        'name': 'Sample Data',
        'description': 'This is a sample API response.'
    }
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def create_data():
    # Retrieve data from the request
    new_data = request.json
    response = {
        'message': 'Data created successfully',
        'data': new_data
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
