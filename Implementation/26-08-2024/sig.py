from flask import Flask, request, jsonify
import oqs
from pprint import pprint

app = Flask(__name__)

@app.route('/api/sign', methods=['POST'])
def sign_message():
    try:
        # Extract message from the request
        data = request.json
        if 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message'].encode()

        # Create signer with selected signature mechanism
        sigalg = "Dilithium2"
        with oqs.Signature(sigalg) as signer:
            print("\nSignature details:")
            pprint(signer.details)

            # Generate keypair for the signer
            signer_public_key = signer.generate_keypair()
            # Sign the message
            signature = signer.sign(message)
            
            # Return the public key and signature
            return jsonify({
                'public_key': signer_public_key.decode(),  # Encode public key if necessary
                'signature': signature.decode()  # Encode signature if necessary
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify', methods=['POST'])
def verify_signature():
    try:
        # Extract data from the request
        data = request.json
        if 'message' not in data or 'signature' not in data or 'public_key' not in data:
            return jsonify({'error': 'Message, signature, or public_key not provided'}), 400
        
        message = data['message'].encode()
        signature = data['signature'].encode()
        public_key = data['public_key'].encode()

        # Create verifier with selected signature mechanism
        sigalg = "Dilithium2"
        with oqs.Signature(sigalg) as verifier:
            # Verify the signature
            is_valid = verifier.verify(message, signature, public_key)
            return jsonify({'valid': is_valid})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
