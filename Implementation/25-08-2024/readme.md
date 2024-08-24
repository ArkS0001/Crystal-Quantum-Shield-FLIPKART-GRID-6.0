https://stackoverflow.com/questions/78154473/multi-layer-reverse-proxy-nginx

https://github.com/dedoc/scramble/discussions/238

https://scramble.dedoc.co/usage/security

1. Data Filtering

    Input Validation: Ensure that all incoming data is validated according to the expected format, type, and length. This can be done using middleware in your API stack. For example, in Python's Flask or Django, you can use decorators or middleware to validate incoming requests.
    Sanitization: Clean the data by removing or escaping harmful characters that could be used in injection attacks. Libraries like html.escape in Python can help.
    Content Filtering: Implement filtering logic at the API gateway or proxy server (e.g., NGINX) to reject or sanitize unwanted content or harmful requests. NGINX can be configured to inspect and filter incoming HTTP headers and request bodies.

2. Token Scrambling

    Token Generation: Use secure cryptographic methods to generate tokens. These tokens should be unique and securely random. You can use libraries like PyJWT in Python to create JSON Web Tokens (JWT) with strong encryption algorithms.
    Scrambling Process:
        Encrypting Tokens: Use an encryption mechanism like the CRYSTAL-Kyber algorithm to scramble the tokens. Kyber is resistant to quantum attacks, ensuring that tokens are secure even against future quantum threats.
        Token Scrambling at Proxies: Set up proxy servers (e.g., NGINX) to handle token scrambling before forwarding requests to the backend services. This involves intercepting the tokens, scrambling them using encryption, and then transmitting them securely.
    Token Verification: On the receiving end, decrypt the tokens using the corresponding decryption process (e.g., with CRYSTAL-Kyber) and validate them to ensure they haven't been tampered with.

3. Integration Example

    Middleware Implementation:
        In your API application, implement middleware for token scrambling and filtering. For instance, in a Flask application, you could write a middleware that intercepts incoming requests, scrambles the tokens using an encryption library, and then processes the request.
    NGINX Configuration:
        Use NGINX as a reverse proxy to apply filtering rules and scramble tokens before requests reach your application server. You can use Lua scripting in NGINX to perform complex token handling or filtering logic.

4. Monitoring and Logging

    Implement logging mechanisms to track scrambled tokens and filtered data. Use tools like Prometheus and Grafana for real-time monitoring and visualization of API security events, as mentioned in your document.

5. Continuous Security

    Integrate these security measures into your CI/CD pipeline to ensure they are automatically tested and deployed. Use containerization tools like Docker and orchestration platforms like Kubernetes to manage these security features effectively.
