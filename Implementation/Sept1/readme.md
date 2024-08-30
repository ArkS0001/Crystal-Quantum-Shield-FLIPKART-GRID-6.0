https://www.genre.com/us/knowledge/publications/2023/september/the-future-of-cryptography-and-quantum-computing-en

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
