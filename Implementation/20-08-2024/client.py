import requests
from kyber import Kyber512

# API URL for the local Flask server
api_url = "http://127.0.0.1:5000"

# 1. Retrieve the server's public key
response = requests.get(f'{api_url}/get-public-key')
server_public_key = bytes.fromhex(response.json()['public_key'])

# 2. Encrypt the data using the server's public key
ciphertext, shared_secret = Kyber512.enc(server_public_key)

# 3. Send the encrypted data to the server
response = requests.post(f'{api_url}/secure-data', json={'ciphertext': ciphertext.hex()})

# 4. Receive the server's response
server_response = response.json()
print(f"Server Response: {server_response['message']}")
print(f"Shared Secret: {server_response['shared_secret']}")
