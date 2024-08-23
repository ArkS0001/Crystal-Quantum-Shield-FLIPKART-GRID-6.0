# Signature Python example

import oqs
from pprint import pprint

print("liboqs version:", oqs.oqs_version())
print("liboqs-python version:", oqs.oqs_python_version())
print("Enabled signature mechanisms:")
sigs = oqs.get_enabled_sig_mechanisms()
pprint(sigs, compact=True)

message = "Aakarshit Srivastava".encode()

# Create signer and verifier with sample signature mechanisms
sigalg = "Dilithium2"
with oqs.Signature(sigalg) as signer:
    with oqs.Signature(sigalg) as verifier:
        print("\nSignature details:")
        pprint(signer.details)

        signer_public_key = signer.generate_keypair()
        signature = signer.sign(message)
       # message="chuutiya".encode()
        is_valid = verifier.verify(message, signature, signer_public_key)

        print("\nValid signature?", is_valid)

# import oqs
# from pprint import pprint

# print("liboqs version:", oqs.oqs_version())
# print("liboqs-python version:", oqs.oqs_python_version())
# print("Enabled signature mechanisms:")
# sigs = oqs.get_enabled_sig_mechanisms()
# pprint(sigs, compact=True)

# # Original message to be signed
# original_message = "This is the message to sign".encode()

# # Signature algorithm to use
# sigalg = "Dilithium2"

# # Create signer and verifier with the selected signature mechanism
# with oqs.Signature(sigalg) as signer:
#     with oqs.Signature(sigalg) as verifier:
#         print("\nSignature details:")
#         pprint(signer.details)

#         # Generate key pair
#         keypair = signer.generate_keypair()
        
#         # Inspect the returned keypair to understand its structure
#         print("\nGenerated keypair:", keypair)
        
#         # Depending on the actual return type, handle the keypair appropriately
#         if isinstance(keypair, tuple) and len(keypair) == 2:
#             public_key, secret_key = keypair
#         else:
#             raise ValueError("Unexpected keypair format. Unable to unpack keys.")
        
#         # Sign the original message using the private key
#         signature = signer.sign(original_message)

#         # Verify the signature with the original message
#         is_valid = verifier.verify(original_message, signature, public_key)
#         print("\nValid signature with original message?", is_valid)

#         # Create an intentionally altered message
#         altered_message = "This is an altered message".encode()

#         # Verify the signature with the altered (invalid) message
#         is_valid_invalid_msg = verifier.verify(altered_message, signature, public_key)
#         print("\nValid signature with altered (invalid) message?", is_valid_invalid_msg)
