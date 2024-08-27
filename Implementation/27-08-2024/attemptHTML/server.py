from flask import Flask, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

@app.route('/secure_api', methods=['POST'])
def secure_api():
    api_url = request.json.get('api_url')
    method = request.json.get('method', 'GET')  # GET or POST
    payload = request.json.get('payload', {})  # Payload for POST requests

    # Call the Python script to handle Kyber encryption/decryption
    result = subprocess.run(['python', 'D:/Internship Assignments/Hexon Global Frontend/kem.py'], capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": "Error in processing Kyber algorithm"}), 500

    kyber_output = json.loads(result.stdout)

    # Encrypt the request or response (example, modify based on your needs)
    headers = {
        'Content-Type': 'application/json'
    }
    
    if method == 'POST':
        response = requests.post(api_url, json=payload, headers=headers)
    else:
        response = requests.get(api_url, headers=headers)

    return jsonify({
        'response': response.text,
        'processed_by_kyber': kyber_output
    })

if __name__ == '__main__':
    app.run(debug=True)
