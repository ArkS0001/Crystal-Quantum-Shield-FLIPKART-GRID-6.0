import request

# Define the URL for the API (Layer 1 proxy)
url = "http://localhost:8080/api/data"

# Define the headers, including the Authorization token
headers = {
    "Authorization": "Bearer testtoken123"
}

try:
    # Send the request to the API via the first layer of the proxy
    response = request.get(url, headers=headers)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        print("Response from API: ", response.text)
    else:
        print(f"Failed to get a valid response. Status code: {response.status_code}")
        print("Response text: ", response.text)

except request.exceptions.RequestException as e:
    # Handle any connection errors
    print(f"An error occurred: {e}")
