from flask import Flask, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

@app.route('/secure_api', methods=['POST'])
def secure_api():
    api_url = request.json['api_url']  # API URL provided by the React app

    # Call the separate Python script that handles Kyber encryption/decryption
    result = subprocess.run(['python3', '/path/to/kem.py'], capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": "Error in processing Kyber algorithm"}), 500

    # The output from the Python script
    kyber_output = json.loads(result.stdout)
    shared_secret = bytes.fromhex(kyber_output['shared_secret'])

    # Example: Make a request to the provided API URL using the shared secret or other processing
    response = requests.get(api_url)

    # Assume that you process the response using the shared secret (e.g., encrypting it)
    # For simplicity, let's assume we're sending the response directly back
    return jsonify({
        'response': response.text,
        'processed_by_kyber': kyber_output
    })

if __name__ == '__main__':
    app.run(debug=True)
