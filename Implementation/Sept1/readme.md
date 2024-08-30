https://www.genre.com/us/knowledge/publications/2023/september/the-future-of-cryptography-and-quantum-computing-en
# IMPORTANT POINTS FOR VIDEO
1. Quantum Computing Overview

    Quantum computing leverages quantum mechanics principles like superposition and entanglement to perform computations far faster than classical computers.
    Qubits allow quantum computers to represent multiple states simultaneously, providing exponential speedup for certain types of problems.

2. Quantum Algorithms

    Shor’s algorithm: Efficiently solves integer factorization and discrete logarithms, breaking RSA encryption by factoring large semiprime numbers in polynomial time.
    Grover’s algorithm: Offers a quadratic speedup for searching unsorted databases, affecting symmetric encryption like AES but can be mitigated by increasing key sizes.

3. Cryptography and Quantum Threat

    Asymmetric encryption (e.g., RSA) relies on the difficulty of factoring large numbers. Shor’s algorithm poses a direct threat to it by efficiently solving this problem.
    Symmetric encryption (e.g., AES) is less vulnerable but could be weakened by Grover’s algorithm, which can halve the effective key size (e.g., 256-bit AES would offer 128-bit security).

4. Attack on RSA using Shor’s Algorithm

    RSA encryption relies on large semiprime numbers for security.
    Shor’s algorithm enables quantum computers to factor large numbers in polynomial time, rendering RSA insecure.
    Once quantum computers mature, they will be able to break RSA encryption within hours or days, compromising its security.

5. Quantum Threat Timeline

    Current quantum computers are still limited in terms of qubit count and error correction, unable to factor large numbers used in RSA.
    Large-scale quantum computers capable of breaking RSA are expected to be developed within the next two decades.

6. Post-Quantum Cryptography (PQC)

    Post-quantum cryptography focuses on developing encryption schemes resistant to quantum attacks.
    NIST’s PQC candidates (e.g., Kyber for key exchange, Dilithium for digital signatures) are designed to resist attacks from quantum computers.
    Organizations should begin adopting quantum-resistant algorithms to future-proof their data against quantum threats.

7. Mitigating AES Attacks

    AES is relatively more secure against quantum threats but requires longer key sizes (e.g., 256-bit) to defend against Grover's algorithm.

8. “Harvest Now, Decrypt Later” Threat

    Adversaries might store classically encrypted data to decrypt it later once quantum computers become powerful enough, posing a serious long-term risk to sensitive information.

Conclusion:

    Quantum computing threatens current encryption standards, particularly RSA and other asymmetric systems.
    Transitioning to post-quantum cryptography like Kyber and Dilithium is crucial for long-term data security.
    Organizations must assess their cryptographic strategies and prepare for a post-quantum future to mitigate these risks.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Quantum Preparedness

There are two crucial aspects to quantum preparedness:

    Pre-emptive Post-Quantum Cryptography Implementation: This refers to transitioning to encryption systems that are resistant to quantum attacks before quantum computers can undermine classical cryptography.
    "Harvest Now, Decrypt Later" Threat: This is the pressing concern where attackers may harvest encrypted data now, planning to decrypt it later once quantum computers become powerful enough. This is particularly important for industries, like insurance, where data retention spans decades.

Quantum Computing Overview

Quantum computing leverages the principles of quantum mechanics using qubits, which differ from classical bits because they can exist in multiple states (superposition). This leads to faster computations for specific problems:

    Grover's algorithm enables faster database searches.
    Shor's algorithm can break classical cryptographic systems, especially those based on prime factorization like RSA.

Classical Cryptography and Quantum Threat

Classical cryptography uses two main methods:

    Symmetric Encryption: Faster but requires secure key distribution (e.g., AES, 3-DES).
    Asymmetric Encryption: Slower but allows key exchange without secure key distribution (e.g., RSA, ECC).

Quantum computers pose a significant threat to asymmetric encryption, with Shor’s algorithm capable of breaking RSA by factoring large semiprimes, which classical computers find difficult.
Post-Quantum Cryptography (PQC)

To counter these threats, PQC focuses on developing cryptographic methods immune to quantum attacks. NIST has selected the first quantum-resistant algorithms for standardization, including CRYSTALS-Kyber for key exchange, which is based on solving the shortest vector problem (SVP).
Conclusion

Organizations are urged to prepare for the quantum threat by adopting quantum readiness roadmaps and engaging in post-quantum cryptographic strategies. Data secured today might be vulnerable in the future, necessitating early action to ensure long-term protection against quantum computing advancements.
