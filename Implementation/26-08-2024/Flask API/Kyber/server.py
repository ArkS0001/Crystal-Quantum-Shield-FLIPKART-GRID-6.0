from flask import Flask, request, jsonify
import oqs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

app = Flask(__name__)

# In-memory storage for keys and shared secrets (for demonstration purposes)
clients_public_keys = {}
clients_shared_secrets = {}

def encrypt_message(shared_secret, plaintext):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(shared_secret[:32]), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + encryptor.tag + ciphertext

def decrypt_message(shared_secret, ciphertext):
    iv, tag, ciphertext = ciphertext[:12], ciphertext[12:28], ciphertext[28:]
    cipher = Cipher(algorithms.AES(shared_secret[:32]), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

@app.route('/exchange_keys', methods=['POST'])
def exchange_keys():
    client_id = request.json['client_id']
    client_public_key = bytes.fromhex(request.json['public_key'])

    # Server generates its KEM keypair
    kemalg = "Kyber512"
    with oqs.KeyEncapsulation(kemalg) as server:
        # Server encapsulates a shared secret using client's public key
        ciphertext, shared_secret_server = server.encap_secret(client_public_key)
        
        # Store the shared secret for the client
        clients_shared_secrets[client_id] = shared_secret_server

        return jsonify({
            'ciphertext': ciphertext.hex()
        })

@app.route('/secure_api', methods=['POST'])
def secure_api():
    client_id = request.json['client_id']
    ciphertext = bytes.fromhex(request.json['ciphertext'])

    # Retrieve the shared secret for the client
    shared_secret = clients_shared_secrets.get(client_id)
    if not shared_secret:
        return jsonify({"error": "Client not found or key exchange not completed"}), 400

    # Decrypt the client's message
    decrypted_message = decrypt_message(shared_secret, ciphertext)

    # Process the request (here we just echo the message)
    response_message = f"Server received: {decrypted_message.decode()}"

    # Encrypt the response
    encrypted_response = encrypt_message(shared_secret, response_message.encode())

    return jsonify({
        'response_ciphertext': encrypted_response.hex()
    })

if __name__ == '__main__':
    app.
