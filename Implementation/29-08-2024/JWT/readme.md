Running the Setup

    Start NGINX:

        Ensure nginx.conf is configured in the C:\nginx\conf directory.

  Start NGINX:

        

    cd C:\nginx
    start nginx

Run the Flask App:

  Make sure the Flask app is running on port 5000:

    

    python app.py

Install the requests Library:

If you haven’t installed it:


    pip install requests

Run the Test Script:

  Execute the script to test token generation and API call:


        python api_request.py

Summary

    Flask App (app.py): Handles JWT creation and validation.
    NGINX Configuration (nginx.conf): Configured to forward JWTs and apply additional layers of security.
    Test Script (api_request.py): Requests a token and uses it to access a secured endpoint.
