# PQC-Sentry
Autonomous AI-driven post-quantum migration engine designed to identify legacy cryptographic primitives (RSA, ECC, 3DES) and contextually auto-patch them with NIST-approved ML-KEM (Kyber) primitives. Built for advanced crypto-agility assessment.
# PQC-Sentry: Autonomous Post-Quantum Cryptography Migration Engine

PQC-Sentry is an enterprise-grade cybersecurity infrastructure tool designed to automate **Cryptographic Agility**. It programmatically identifies quantum-vulnerable cryptographic configurations (such as RSA, Diffie-Hellman, and Triple-DES) within application source code and executes seamless, context-aware runtime structural rewrites using NIST-approved post-quantum algorithms like **ML-KEM (Kyber-768)**.

Developed specifically to bridge the legacy-to-quantum transition gap between 2026 and 2030, this engine focuses on zero-developer-overhead asset protection against the "Harvest Now, Decrypt Later" threat index.

---

## ⚡ Key Capabilities
* **Static Application Security Testing (SAST):** Highly optimized multi-language mapping of encryption packages (Python, C++, Go).
* **Context-Aware Splicing Engine:** Surgical Abstract Syntax Tree (AST) and token regex parsing to overwrite vulnerable parameters without destroying business logic loops.
* **Deterministic Backups:** Instantiates immutable `.bak` records before system modifications.

---

## 🏗️ Architectural Flow
[Target Source Code] ──► [Component A: SAST Scan Engine] ──► [Structured Vulnerability Report (JSON)]
│
▼
[Quantum-Safe Application] ◄── [Component B: Liboqs Interface] ◄── [Component C: Auto-Patcher]
