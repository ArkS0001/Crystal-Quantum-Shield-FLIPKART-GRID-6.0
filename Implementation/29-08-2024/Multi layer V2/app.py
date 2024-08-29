# from flask import Flask, jsonify, request
# import request
# import base64

# app = Flask(__name__)

# def unscramble_token(scrambled_token):
#     # Unscramble the token (Base64 decoding)
#     try:
#         return base64.b64decode(scrambled_token).decode('utf-8')
#     except Exception as e:
#         return None

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     # Extract and unscramble the token from X-Scrambled-Token header
#     scrambled_token = request.headers.get('X-Scrambled-Token')
#     if scrambled_token:
#         token = unscramble_token(scrambled_token)
#         if not token:
#             return jsonify({"error": "Invalid scrambled token"}), 400
#         print(f"Unscrambled token: {token}")
#     else:
#         return jsonify({"error": "No token provided"}), 400

#     # Simulate an API call (You can replace this with a real external API call)
#     response = request.get('https://jsonplaceholder.typicode.com/posts')
#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return jsonify({"error": "Failed to fetch data"}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def api_data():
    # Retrieve and print the scrambled token
    scrambled_token = request.headers.get('X-Scrambled-Token', 'No Token Provided')
    print(f"Scrambled token received: {scrambled_token}")
    
    # Respond with a simple message
    return jsonify({"message": "hello"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
