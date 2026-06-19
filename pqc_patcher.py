#!/usr/bin/env python3
import os
import shutil
import re
from typing import Tuple

# Standard PQC (ML-KEM / Kyber-768) implementation block template for Python
# Note: In production, this utilizes the local oqs Python bindings wrapper
PQC_TEMPLATE = """# --- PQC MIGRATED START ---
# Vulnerable RSA encryption block auto-replaced with NIST approved ML-KEM (Kyber-768)
from oqs import Kem

try:
    with Kem('Kyber768') as kem:
        public_key, secret_key = kem.generate_keypair()
        ciphertext, shared_secret_alice = kem.encapsulate(public_key)
        shared_secret_bob = kem.decapsulate(secret_key, ciphertext)
        # Quantum-safe shared secret established for payload encryption
except Exception as pqc_err:
    raise RuntimeError(f"PQC Runtime Failure during key encapsulation: {pqc_err}")
# --- PQC MIGRATED END ---"""

def create_backup(file_path: str) -> str:
    """Creates a secure backup of the target file before running surgical patching."""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    return backup_path

def contextual_patch_rsa(file_path: str) -> Tuple[bool, str]:
    """
    Scans the targeted file for legacy RSA usage, isolates the initialization block,
    injects the ML-KEM template contextually, and archives the old implementation.
    """
    if not os.path.exists(file_path):
        return False, "Target file path does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex targeting typical legacy patterns like: rsa.generate_private_key, RSA.generate etc.
    legacy_rsa_pattern = re.compile(
        r'(?:import\s+rsa|from\s+cryptography\..*?\s+import\s+rsa|.*?RSA\.generate.*?)', 
        re.IGNORECASE
    )

    if not legacy_rsa_pattern.search(content):
        return False, "No vulnerable legacy RSA implementation blocks identified."

    # Execute Backup routine immediately before modifying blocks
    try:
        backup_created = create_backup(file_path)
    except Exception as backup_error:
        return False, f"Patching aborted. Backup generation failed: {str(backup_error)}"

    # Parse and safely replace line blocks. 
    # For MVP context routing, we identify the main setup lines and overwrite them cleanly.
    lines = content.splitlines()
    patched_lines = []
    inside_vulnerable_block = False
    block_replaced = False

    for line in lines:
        # Detect legacy imports or generator functions
        if legacy_rsa_pattern.search(line) and not block_replaced:
            patched_lines.append(PQC_TEMPLATE)
            block_replaced = True
            # Skip appending the current legacy line
            continue
        
        # If we encounter multi-line RSA blocks, skip them structural-wise to clean up the code
        if ("rsa" in line.lower() or "pkcs1" in line.lower()) and block_replaced:
            # Drop legacy assignments to prevent variable collision with new ML-KEM structure
            if any(x in line for x in ["key =", "private_key", "public_key"]):
                continue

        patched_lines.append(line)

    # Re-write the production file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(patched_lines))

    return True, f"Successfully patched file. Original codebase backed up to: {backup_created}"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PQC-Sentry Target Auto-Patching Engine")
    parser.add_argument("file", help="Path to the target vulnerable Python source file.")
    args = parser.parse_args()

    print(f"[*] Analyzing target file context: {args.file}")
    success, message = contextual_patch_rsa(args.file)
    
    if success:
        print(f"[+] SUCCESS: {message}")
    else:
        print(f"[-] FAILED: {message}")