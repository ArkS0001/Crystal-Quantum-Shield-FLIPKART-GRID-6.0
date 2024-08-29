#api_request.py

import requests

# Define the URL for the token endpoint
token_url = "http://localhost:8080/token"

# Define the payload to request a token
payload = {
    "user_id": "test_user"
}

# Request a JWT token
response = requests.post(token_url, json=payload)
if response.status_code == 200:
    token = response.json().get('token')
    print(f"JWT Token: {token}")

    # Define the URL for the API (Layer 1 proxy)
    api_url = "http://localhost:8080/api/data"

    # Define the headers with the JWT token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Make the request to the API endpoint
    api_response = requests.get(api_url, headers=headers)
    if api_response.status_code == 200:
        print("Response from API: ", api_response.json())
    else:
        print(f"Failed to get a valid response. Status code: {api_response.status_code}")
        print("Response text: ", api_response.text)
else:
    print(f"Failed to get a token. Status code: {response.status_code}")
    print("Response text: ", response.text)
