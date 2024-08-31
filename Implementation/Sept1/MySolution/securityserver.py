from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint for logging and checking API calls
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

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)
