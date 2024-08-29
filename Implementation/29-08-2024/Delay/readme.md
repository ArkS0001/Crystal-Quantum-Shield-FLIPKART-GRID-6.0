Yes, you can add delays at different proxy levels in NGINX to simulate latency and check for attacks or abuse. This can be useful for stress testing, rate limiting, and ensuring that your system handles various scenarios gracefully. If a time limit is exceeded, you can configure NGINX to refuse the connection.
Steps to Add Delays and Handle Time Limits

    Add Delays at Different Proxy Levels
    Configure Time Limits and Refusal Logic
    Test the Configuration

1. Add Delays at Different Proxy Levels

You can use the limit_req module to add delays and implement rate limiting. The limit_req_zone and limit_req directives can be used to control request rates, and you can use proxy_pass with proxy_set_header for forwarding requests.
nginx.conf

nginx

worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    # Logging configuration
    access_log  logs/access.log;
    error_log   logs/error.log;

    # Increase timeouts (optional)
    send_timeout 60s;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Gzip compression settings (optional)
    gzip on;
    gzip_types text/plain application/xml text/css application/json application/javascript text/javascript;

    # Delay settings
    # Layer 1 Proxy (Token Scrambling or Forwarding)
    server {
        listen 8080;
        server_name localhost;

        # Define delay (simulate latency)
        location / {
            set $delay 0s;
            # Add delay
            if ($request_uri ~* "/api/data") {
                set $delay 2s;  # Simulate 2 seconds delay for /api/data
            }
            # Delay request processing
            add_header X-Delay $delay;
            access_log logs/access.log delay=0s;
            # Forward request to Layer 2 Proxy
            proxy_pass http://127.0.0.1:8081;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Authorization $http_authorization;
        }
    }

    # Layer 2 Proxy (Rate Limiting and IP Filtering)
    server {
        listen 8081;

        # Define rate limiting zone
        limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

        location / {
            # Apply rate limiting
            limit_req zone=mylimit burst=20 nodelay;
            # Delay processing (simulate latency)
            set $delay 1s;
            if ($request_uri ~* "/api/data") {
                set $delay 1s;  # Simulate 1 second delay for /api/data
            }
            # Delay request processing
            access_log logs/access.log delay=1s;
            # Allow only specific IP ranges (adjust as needed)
            allow 192.168.1.0/24;  # Example IP range (whitelisted)
            deny all;  # Deny all other IP addresses

            # Forward request to Layer 3 Proxy
            proxy_pass http://127.0.0.1:8082;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

    # Layer 3 Proxy (API Gateway - Forwarding to Flask App)
    server {
        listen 8082;

        # Delay processing (simulate latency)
        location / {
            set $delay 500ms;
            if ($request_uri ~* "/api/data") {
                set $delay 500ms;  # Simulate 500ms delay for /api/data
            }
            # Delay request processing
            access_log logs/access.log delay=500ms;
            # Forward the request to the Flask app
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_http_version 1.1;
            proxy_set_header Connection keep-alive;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}

2. Configure Time Limits and Refusal Logic

You can configure timeouts and refusal logic to handle connections that exceed the set time limits.

    Connection Timeout: If the connection to the backend server takes too long, NGINX can be configured to time out and refuse the connection.
    Response Timeout: If the response from the backend server takes too long, NGINX can refuse the connection.

In the configuration above, the proxy_connect_timeout, proxy_send_timeout, and proxy_read_timeout directives are used to specify timeouts.

nginx

    # Increase timeouts
    send_timeout 60s;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

3. Test the Configuration

To test the configuration:

    Reload NGINX to apply the changes:

    bash

    sudo nginx -s reload

    Monitor Logs to verify delays and timeouts:

    Check the access.log and error.log to ensure that the delays and timeouts are working as expected.

    Use curl or Postman to send requests and observe the delays and responses.

By implementing these steps, you can simulate delays at different proxy levels and handle cases where time limits are exceeded by refusing connections or logging errors. This can help in assessing the resilience of your system under various conditions.
