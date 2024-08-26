import requests
import oqs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

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

# Generate client keypair
kemalg = "Kyber512"
client_id = "client123"
with oqs.KeyEncapsulation(kemalg) as client:
    public_key_client = client.generate_keypair()

    # Send public key to server and receive encapsulated secret
    response = requests.post('http://127.0.0.1:5000/exchange_keys', json={
        'client_id': client_id,
        'public_key': public_key_client.hex()
    })
    server_ciphertext = bytes.fromhex(response.json()['ciphertext'])

    # Decapsulate to retrieve shared secret
    shared_secret_client = client.decap_secret(server_ciphertext)

    # Encrypt the message to send to the API
    message = b"Hello, secure server!"
    encrypted_message = encrypt_message(shared_secret_client, message)

    # Send the encrypted message to the server
    response = requests.post('http://127.0.0.1:5000/secure_api', json={
        'client_id': client_id,
        'ciphertext': encrypted_message.hex()
    })

    # Decrypt the server's response
    encrypted_response = bytes.fromhex(response.json()['response_ciphertext'])
    decrypted_response = decrypt_message(shared_secret_client, encrypted_response)
    print(f"Decrypted server response: {decrypted_response.decode()}")
