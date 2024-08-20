from flask import Flask, request, jsonify
from kyber import Kyber512

app = Flask(__name__)

# Generate server's key pair
server_public_key, server_private_key = Kyber512.keygen()

@app.route('/get-public-key', methods=['GET'])
def get_public_key():
    # Provide the server's public key to the client
    return jsonify({'public_key': server_public_key.hex()})

@app.route('/secure-data', methods=['POST'])
def secure_data():
    # Receive encrypted data from the client
    data = request.json
    ciphertext = bytes.fromhex(data['ciphertext'])

    # Decrypt the data using the server's private key
    shared_secret = Kyber512.dec(ciphertext, server_private_key)

    # Respond with a success message and the shared secret
    return jsonify({'message': 'Data received and decrypted successfully.', 'shared_secret': shared_secret.hex()})

if __name__ == '__main__':
    app.run(debug=True)
