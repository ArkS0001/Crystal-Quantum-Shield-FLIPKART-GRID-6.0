import oqs
import json

def run_kyber_algorithm():
    kemalg = "Kyber512"
    with oqs.KeyEncapsulation(kemalg) as client:
        with oqs.KeyEncapsulation(kemalg) as server:
            # Client generates its keypair
            public_key_client = client.generate_keypair()

            # The server encapsulates its secret using the client's public key
            ciphertext, shared_secret_server = server.encap_secret(public_key_client)

            # The client decapsulates the server's ciphertext to obtain the shared secret
            shared_secret_client = client.decap_secret(ciphertext)

            # Verify the shared secrets match
            shared_secrets_match = shared_secret_client == shared_secret_server

            # Output the results in a format the Flask server can parse
            output = {
                'public_key_client': public_key_client.hex(),
                'ciphertext': ciphertext.hex(),
                'shared_secret': shared_secret_client.hex(),
                'shared_secrets_match': shared_secrets_match
            }
            print(json.dumps(output))

if __name__ == "__main__":
    run_kyber_algorithm()
