import oqs
import binascii
# def sign_message(message):
#     sigalg = "Dilithium2"
#     with oqs.Signature(sigalg) as signer:
#         # Generate a key pair
#         public_key, secret_key = signer.generate_keypair()

#         # Sign the message
#         signature = signer.sign(message.encode())

#         # Return public key and signature in hex format
#         return {
#             "signer_public_key": public_key.hex(),
#             "secret_key": secret_key.hex(),  # Optionally return the secret key if needed
#             "signature": signature.hex()
#         }

# def verify_signature(message, signature, public_key_hex):
#     sigalg = "Dilithium2"
#     with oqs.Signature(sigalg) as verifier:
#         # Convert inputs from hex to bytes
#         public_key = bytes.fromhex(public_key_hex)
#         signature_bytes = bytes.fromhex(signature)

#         # Verify the signature
#         is_valid = verifier.verify(message.encode(), signature_bytes, public_key)

#         return {"is_valid": is_valid}


def sign_message(message):
    sigalg = "Dilithium2"
    with oqs.Signature(sigalg) as signer:
        signer_public_key = signer.generate_keypair()
        signature = signer.sign(message.encode())

        return {
            "signer_public_key": signer_public_key.hex(),
            "signature": signature.hex()
        }

def verify_signature(message, signature, signer_public_key):
    sigalg = "Dilithium2"
    with oqs.Signature(sigalg) as verifier:
        is_valid = verifier.verify(message.encode(), binascii.unhexlify(signature), binascii.unhexlify(signer_public_key))
        print(f"Is valid: {is_valid} ")
        return {"is_valid": is_valid}
    

message = "hello"
result = sign_message(message)
public_key = result['signer_public_key']
signature = result['signature']

# Now verify
verification_result = verify_signature(message, signature, public_key)
print("Is the signature valid?", verification_result['is_valid'])
