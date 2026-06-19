# TECHNICAL WHITEPAPER
## PQC-Sentry: Autonomous Cryptographic Agility and Automated Post-Quantum Migration

**Author:** Soumitro Baral Supto  
**Date:** June 2026  
**Classification:** Open Source Security Infrastructure / Sovereign Dominance Framework  

---

### Abstract
The imminent advent of cryptanalytically relevant quantum computers (CRQCs) poses an existential threat to global cryptographic infrastructures. Legacy asymmetric primitives, specifically RSA, Finite Field Diffie-Hellman, and Elliptic Curve Cryptography (ECC), will succumb to Shor’s algorithm, collapsing the foundational trust layers of banking, military communications, and cloud architectures. 

This paper introduces **PQC-Sentry**, an enterprise-grade, autonomous migration engine designed to inject cryptographic agility into legacy systems. PQC-Sentry combines high-performance Static Application Security Testing (SAST) with an automated, context-aware AST/Regex rewriting engine. By programmatically deprecating quantum-vulnerable algorithms and surgically splicing NIST-approved Post-Quantum Cryptography (PQC) standards—specifically **ML-KEM (Kyber-768)** and **ML-DSA (Dilithium)**—PQC-Sentry mitigates the "Harvest Now, Decrypt Later" paradigm with zero manual developer overhead.

---

### 1. The Core Architecture & Pipeline

PQC-Sentry operates as a non-disruptive pipeline that transitions codebases from legacy configurations to fully post-quantum compliant states through three decoupled modules:

* **MODULE A: Static Analysis & Cryptographic Mapping**
  * Abstract Syntax Tree (AST) & Tokenization Patterns
  * Locates RSA, SHA-1, 3DES, Triple-DES instances
* **MODULE C: Contextual Rewriting Engine**
  * State-preserving file backup initialization (.bak)
  * Code isolation & automated token splicing
* **MODULE B: Liboqs Runtime Compilation Backend**
  * Integrates Open Quantum Safe (OQS) bindings
  * Instantiates ML-KEM-768 for Encapsulated Exchange

---

### 2. Experimental Verification & Production Validation

To prove the feasibility of autonomous patching, an MVP prototype was executed against a live target script (`vulnerable_app.py`) running a legacy 2048-bit RSA configuration. 

#### 2.1 Pre-Migration State
```python
from cryptography.hazmat.primitives.asymmetric import rsa
# Generates legacy vulnerable asymmetric key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
