from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy users data
users = {
    'admin': 'password123',
    'user': 'userpass'
}

@app.route('/api/security/login', methods=['POST'])
def login_security():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    print(f"Login attempt: Username={username}")
    
    if username in users and users[username] == password:
        print("Login successful")
        return jsonify({'message': 'Login successful'}), 200
    else:
        print("Login failed")
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/security/logout', methods=['POST'])
def logout_security():
    data = request.json
    username = data.get('username')
    
    print(f"Logout attempt: Username={username}")
    
    # Implement any necessary logout logic here
    print("Logout successful")
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
