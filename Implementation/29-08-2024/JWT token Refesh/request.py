import requests

# Define URLs for token and API endpoints
token_url = "http://localhost:8080/token"
refresh_url = "http://localhost:8080/refresh"
api_url = "http://localhost:8080/api/data"

def get_token():
    payload = {"user_id": "test_user"}
    response = requests.post(token_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get a token. Status code: {response.status_code}")
        print("Response text: ", response.text)
        return None

def refresh_token(refresh_token):
    response = requests.post(refresh_url, json={"refresh_token": refresh_token})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Failed to refresh token. Status code: {response.status_code}")
        print("Response text: ", response.text)
        return None

def make_api_request(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        print("Response from API: ", response.json())
    else:
        print(f"Failed to get a valid response. Status code: {response.status_code}")
        print("Response text: ", response.text)

# Main script logic
tokens = get_token()
if tokens:
    access_token = tokens.get('token')
    refresh_token = tokens.get('refresh_token')

    # Make the initial API request
    make_api_request(access_token)

    # Simulate an expired token scenario
    print("\nSimulating token refresh...\n")

    # Refresh the access token
    new_access_token = refresh_token(refresh_token)
    if new_access_token:
        make_api_request(new_access_token)
