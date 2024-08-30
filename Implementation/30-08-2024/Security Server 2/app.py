from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a strong secret key

SECURITY_SERVER_URL = "http://localhost:5001"

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Send the login data to the security server
        security_response = requests.post(f"{SECURITY_SERVER_URL}/api/security/login", json={'username': username, 'password': password})
        
        if security_response.status_code == 200:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        
        # Notify the security server about the logout
        requests.post(f"{SECURITY_SERVER_URL}/api/security/logout", json={'username': username})
        
        session.pop('username', None)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
