from flask import Flask, render_template, request, jsonify
import oqs
from kyber import perform_key_exchange
from dilithium import sign_message, verify_signature

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/key-exchange', methods=['POST'])
def key_exchange():
    result = perform_key_exchange()
    return jsonify(result)

# @app.route('/api/sign-message', methods=['POST'])
# def sign_message():
#     data = request.json
#     message = data.get('message')

#     if not message:
#         return jsonify({'error': 'Message is required'}), 400

#     try:
#         result = sign_message(message)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/verify-signature', methods=['POST'])
# def verify_signature():
#     data = request.json
#     message = data.get('message')
#     signature = data.get('signature')
#     public_key = data.get('public_key')

#     if not message or not signature or not public_key:
#         return jsonify({'error': 'Message, signature, and public_key are required'}), 400

#     try:
#         result = verify_signature(message, signature, public_key)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/signature', methods=['POST'])
def sign_message_route():
    data = request.json
    message = data.get('message', '')
    result = sign_message(message)
    return jsonify(result)

@app.route('/api/verify-signature', methods=['POST'])
def verify_signature_route():
    data = request.json
    message = data.get('message', '')
    signature = data.get('signature', '')
    signer_public_key = data.get('signer_public_key', '')

    print(f"Message: {message}")
    print(f"Signature: {signature}")
    print(f"Signer Public Key: {signer_public_key}")

    result = verify_signature(message, signature, signer_public_key)
    return jsonify(result)

# def sign_message(message):
#     sigalg = "Dilithium2"
#     with oqs.Signature(sigalg) as signer:
#         signer_public_key = signer.generate_keypair()
#         signature = signer.sign(message.encode())

#         return {
#             "signer_public_key": signer_public_key.hex(),
#             "signature": signature.hex()
#         }

# def verify_signature(message, signature, signer_public_key):
#     sigalg = "Dilithium2"
#     with oqs.Signature(sigalg) as verifier:
#         print(f"Verifying with Signature: {signature} and Public Key: {signer_public_key}")
#         is_valid = verifier.verify(
#             message.encode(), 
#             bytes.fromhex(signature), 
#             bytes.fromhex(signer_public_key)
#         )

#         print(f"Is signature valid? {is_valid}")

#         return {"is_valid": is_valid}

if __name__ == '__main__':
    app.run(debug=True)
