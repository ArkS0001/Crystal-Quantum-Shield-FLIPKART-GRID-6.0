# Crystal Quantum Shield: post quantum cryptography security solution for API security

![Untitled](https://github.com/user-attachments/assets/fc3587cb-9a89-4032-aac8-bdca2334fa0c)
![Untitled](https://github.com/user-attachments/assets/f5b0646a-7ab5-4012-b032-1f6915f0fc5c)


## Citations
Tripathi, T., Awasthi, A., Singh, S. P., & Chaturvedi, A. (2024, March 28). Post Quantum Cryptography and its Comparison with Classical Cryptography. arXiv.org. https://arxiv.org/abs/2403.19299 

Avanzi, R., Bos, J., Ducas, L., Kiltz, E., Lepoint, T., Lyubashevsky, V., Schanck, J. M., Schwabe, P., Seiler, G., & Stehlé, D. (2021). CRYSTALS-Kyber Algorithm Specifications And Supporting Documentation (version 3.02). https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf

Bavdekar, R., Chopde, E. J., Bhatia, A., Tiwari, K., Daniel, S. J., & Atul. (2022). Post Quantum Cryptography: techniques, challenges, standardization, and directions for future research. arXiv (Cornell University). https://doi.org/10.48550/arxiv.2202.02826

CSIRT-Fin, CERT-In, & Mastercard. (2023). API Security: Threats, Best Practices, Challenges, and Way forward using AI.https://www.csk.gov.in/documents/CIWP-2023-0001.pdf.

Qazi, F. (2023). Application Programming Interface (API) security in cloud applications. EAI Endorsed Transactions on Cloud Systems, 7(23), e1. https://doi.org/10.4108/eetcs.v7i23.3011

Sconiers-Hasan, M. & CERT® Division. (2024). Application Programming Interface (API) vulnerabilities and risks (SPECIAL REPORT CMU/SEI-2024-SR-004). Carnegie Mellon University. https://doi.org/10.1184/R1/25282342

Ducas, L., Kiltz, E., Lepoint, T., Lyubashevsky, V., Schwabe, P., Seiler, G., & Stehlé, D. (2018). CRYSTALS-Dilithium: a Lattice-Based digital signature scheme. tches.iacr.org. https://doi.org/10.13154/tches.v2018.i1.238-268

Sailada, S., Vohra, N., & Subramanian, N. (2022). Crystal Dilithium Algorithm for Post Quantum Cryptography:Experimentation and Usecase for eSign. 2022 First International Conference on Electrical, Electronics, Information and Communication Technologies (ICEEICT), 1–6. https://doi.org/10.1109/iceeict53079.2022.9768654

Hughes, Richard J., D.M. Alde, P. Dyer, G.G.Luther, G.L. Morgan, and M. Schauer, Quantum
cryptography, Contemporary Physics, Vol. 36, No. 3 (1995).

[2] A. Chaturvedi, N. Srivastava, V. Shukla, A secure wireless communication protocol using DiffieHellman key exchange, International journal of computer applications, volume 126, number 5,
2015, 35-38, DOI: 10.5120/ijca2015906060

[3] V. Shukla, A. Chaturvedi, N. Srivastava, Nanotechnology and cryptographic protocols: issues
and possible solutions, Nanomaterials and energy, volume 8, issue 1, 2019, 1-6, DOI:
10.1680/jnaen.18.00006

M.K. Misra, A. Chaturvedi, S.P. Tripathi, V. Shukla, A unique key sharing protocol among
three users using non-commutative group for electronic health record system, Journal of discrete mathematical sciences and cryptography, volume 22, issue 8, 2019, 1435–1451, DOI:
10.1080/09720529.2019.1692450

[11] A. Chaturvedi, V. Shukla, M.K. Misra, Three party key sharing protocol using polynomial rings,
5th IEEE Uttar Pradesh Section International Conference on Electrical, Electronics and Computer
Engineering (UPCON), 2018, 1-5, DOI: 10.1109/UPCON.2018.8596905

Applied Cryptography, Second Edition: Protocols, Algorithms, and Source Code in C (cloth)
Author(s): Bruce Schneier.

[15] A. Awasthi, A. Chaturvedi, Cryptography: Classical versus Post-Quantum, Cornell university
arxiv, 2024, DOI: https://doi.org/10.48550/arXiv.2402.10988

[16] Pranjal, A. Chaturvedi, Post-Quantum Cryptography, Cornell university arxiv, 2024, DOI:
https://doi.org/10.48550/arXiv.2402.10576

[17] FIPS. 46-3, ‘“Data Encryption Standard,” Federal Information Processing Standard (FIPS), Publication 46-3, National Bureau of Standards, US. Department of Commerce, Washington D.C.,
October 25, 1999.

Charles H. Bennett, Gilles Brassard, and Artur K. Ekert ”Quantum Cryptography”, Scientific
American 267:4, (October 1992).

Affordable Quantum Cryptography http://www.siemens.com/innovation/apps/pof micr
osite/ pof-spring2009/ html en/interviewchristianmonyk.htm




# **Algorithm for Crystal Quantum Shield (C.Q.S) Flow**

1. **Start**  
   - Receive incoming requests from the host (e.g., Login, Product Search, Payment).

2. **Pass Through API Gateway**  
   - Route the request to the Crystal Quantum Shield (C.Q.S) for processing.

3. **Authentication**  
   - Validate user identity using **Crystal Dilithium**:
     - Generate a signature \((z, h)\) where \(z = c \cdot s_1 + y\) and \(h\) is computed via hashing.  
     - Verify signature using public key \((t_1, h)\): \(||z||_\infty < \beta\) and hash consistency with \(t_1\).
   - If authentication fails, log the failure and discard the request.

4. **Encryption**  
   - Encrypt data using **Crystal Kyber**:
     - Generate shared secret \(K\) via key encapsulation: \(K = H(ss)\), where \(ss = H(pk \cdot sk + noise)\).  
     - Use encapsulated key for symmetric encryption.
   - Ensure secure communication between host and server.

5. **Role-Based Access Control (RBAC)**  
   - Check user permissions and roles to validate access.  
   - Apply rate limiting and data filtering based on policies.  
   - If access is denied, log and discard the request.

6. **Reverse Proxy with Multi-Layer Security**  
   - Route the request through multi-layer proxy servers.  
   - Perform additional checks:
     - **Filtering**: Analyze request content.
     - **Modify IP Header**: Adjust headers for security.
     - **Token Scramble**: Encrypt tokens for further validation.
     - **Add Delay**: Introduce latency if suspicious patterns are detected.

7. **Endpoint Monitoring**  
   - Continuously monitor requests and responses for anomalies.

8. **Whitelist and Blacklist Validation**  
   - Compare requests against whitelist and blacklist rules.  
   - If on blacklist, log and discard the request.  
   - If on whitelist, allow further processing.

9. **Data Flow Validation**  
   - Validate JSON Web Token (JWT) for integrity.  
   - Accept data flow if all checks pass.

10. **Logging and Monitoring**  
    - Log all requests and their statuses (passed, failed, filtered, etc.).  
    - Send logs to the monitoring system for visualization.

11. **Fine-Tuned Deep Learning Model**  
    - Analyze logs and request patterns using a trained model.  
    - Generate insights and alerts for anomalies.

12. **Dashboard Monitoring and Alerts**  
    - Visualize data metrics and send alerts for suspicious activities.

13. **Response to End User**  
    - If all validations succeed, forward the response to the API Gateway for delivery to the end user.

14. **End**  
   - If any step fails, discard the request and log the failure.
