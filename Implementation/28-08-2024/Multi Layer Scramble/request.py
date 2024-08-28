# import requests

# def fetch_data():
#     url = 'https://jsonplaceholder.typicode.com/posts/1'  # Example API endpoint
#     headers = {'Authorization': 'Bearer <your_token_here>'}
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {'error': 'Failed to fetch data'}
# import requests

# def fetch_data(url, token):
#     headers = {'Authorization': f'Bearer {token}'}
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {'error': f'Failed to fetch data from {url}'}

# def make_requests():
#     urls = [
#         'http://localhost/api/posts/1',
#         'http://localhost/api/posts/2',
#         'http://localhost/api/posts/3'
#     ]
    
#     tokens = [
#         'token123',
#         'anotherToken456',
#         'yetAnotherToken789'
#     ]
    
#     proxy_jumps = [
#         'http://localhost:8082',  # Main server with token scrambling (level 1)
#         'http://localhost:8081',  # Level 2 proxy
#         'http://localhost:5000'   # Flask backend (final destination)
#     ]

#     for url, token in zip(urls, tokens):
#         print(f"\nMaking request to {url} with token: {token}")
#         response_data = fetch_data(url, token)
#         print(f"Response Data: {response_data}")

#         print("Proxy jumps:")
#         for proxy in proxy_jumps:
#             print(f"  - Passed through: {proxy}")
#         print("\n" + "="*40)

# if __name__ == "__main__":
#     make_requests()


import requests

def fetch_data(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Failed to fetch data from {url}'}

def make_requests():
    urls = [
        'http://localhost/api/data',
        'http://localhost/api/data',
        'http://localhost/api/data'
    ]
    
    tokens = [
        'token123',
        'anotherToken456',
        'yetAnotherToken789'
    ]
    
    proxy_jumps = [
        'http://localhost:8082',  # Main server with token scrambling (level 1)
        'http://localhost:8081',  # Level 2 proxy
        'http://localhost:5000'   # Flask backend (final destination)
    ]

    for url, token in zip(urls, tokens):
        print(f"\nMaking request to {url} with token: {token}")
        response_data = fetch_data(url, token)
        print(f"Response Data: {response_data}")

        print("Proxy jumps:")
        for proxy in proxy_jumps:
            print(f"  - Passed through: {proxy}")
        print("\n" + "="*40)

if __name__ == "__main__":
    make_requests()
