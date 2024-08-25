```
+------------------------------------------------------+
|                     Client                           |
+------------------------------------------------------+
| 1. Request Secure Session                            |
|                                                      |
| 2. Receive Server's Kyber Public Key                 |
|                                                      |
| 3. Generate Symmetric Key                            |
|    - Encrypt with Kyber Public Key                   |
|    - Send Encrypted Symmetric Key                    |
|                                                      |
| 5. Encrypt API Requests/Data with Symmetric Key      |
+------------------------------------------------------+
             |                                  
             |                                  
             V                                  
+------------------------------------------------------+
|                     Server                           |
+------------------------------------------------------+
| 2. Send Kyber Public Key                             |
|                                                      |
| 3. Receive Encrypted Symmetric Key                   |
|    - Decrypt with Kyber Private Key                  |
|                                                      |
| 4. Establish Secure Session with Symmetric Key       |
|                                                      |
| 5. Decrypt API Requests/Data with Symmetric Key      |
+------------------------------------------------------+
```

# Diagram Description
1. Client Requests Secure Connection:

    Step 1: The client initiates a connection to the API server and requests a secure session.

2. Server Responds with Crystal Kyber Public Key:

    Step 2: The server responds by sending its Crystal Kyber public key to the client.

3. Key Exchange using Crystal Kyber:

    Step 3:
        The client generates a symmetric key.
        The client uses the server's Crystal Kyber public key to encrypt this symmetric key.
        The encrypted symmetric key is sent back to the server.

4. Secure Session Establishment:

    Step 4:
        The server decrypts the symmetric key using its Crystal Kyber private key.
        Both client and server now have the same symmetric key, which is quantum-resistant due to the Kyber algorithm.

5. Encrypted API Data Communication:

    Step 5:
        The client and server use the symmetric key to encrypt and decrypt API data.
        All data sent over the connection is encrypted, providing end-to-end security.
