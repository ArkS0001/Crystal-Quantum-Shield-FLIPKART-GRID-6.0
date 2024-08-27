import oqs

def perform_key_exchange():
    kemalg = "Kyber1024"
    
    try:
        # Initialize client and server for Kyber key encapsulation
        with oqs.KeyEncapsulation(kemalg) as client:
            with oqs.KeyEncapsulation(kemalg) as server:
                
                # Client generates its keypair
                public_key_client = client.generate_keypair()
                
                # Server encapsulates its secret using the client's public key
                ciphertext, shared_secret_server = server.encap_secret(public_key_client)
                
                # Client decapsulates the server's ciphertext to obtain the shared secret
                shared_secret_client = client.decap_secret(ciphertext)
                
                # Convert keys and secrets to hex for easier debugging and display
                public_key_client_hex = public_key_client.hex()
                ciphertext_hex = ciphertext.hex()
                shared_secret_server_hex = shared_secret_server.hex()
                shared_secret_client_hex = shared_secret_client.hex()
                
                return {
                    "client_public_key": public_key_client_hex,
                    "ciphertext": ciphertext_hex,
                    "shared_secret_server": shared_secret_server_hex,
                    "shared_secret_client": shared_secret_client_hex,
                    "keys_match": shared_secret_client == shared_secret_server,
                }
    
    except Exception as e:
        return {
            "error": str(e)
        }
