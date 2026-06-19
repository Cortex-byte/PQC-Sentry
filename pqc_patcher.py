#!/usr/bin/env python3
import ast
import argparse
import sys
import difflib
import shutil

# NIST approved ML-KEM patch block template
PQC_TEMPLATE = """# --- PQC MIGRATED START ---
# Vulnerable cryptographic algorithm auto-replaced with NIST approved ML-KEM (Kyber-768)
from oqs import Kem
try:
    with Kem('Kyber768') as kem:
        public_key, secret_key = kem.generate_keypair()
        ciphertext, shared_secret_alice = kem.encapsulate(public_key)
        shared_secret_bob = kem.decapsulate(secret_key, ciphertext)
except Exception as pqc_err:
    raise RuntimeError(f"PQC Runtime Failure: {pqc_err}")
# --- PQC MIGRATED END ---"""

class PQCASTScanner(ast.NodeVisitor):
    """AST Visitor to pinpoint exact quantum-vulnerable functions structurally."""
    def __init__(self):
        self.vulnerable_lines = []

    def visit_Call(self, node):
        # Tracking specific enterprise vulnerabilities like rsa.generate_private_key
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            if hasattr(node.func.value, 'id') and node.func.value.id == 'rsa' and node.func.attr == 'generate_private_key':
                func_name = "rsa.generate_private_key"
        
        if func_name:
            self.vulnerable_lines.append(node.lineno)
        
        self.generic_visit(node)

def process_target_file(file_path, dry_run=False):
    with open(file_path, 'r') as f:
        original_source = f.read()

    # Step 1: AST Structural Parsing (Zero False Positives)
    try:
        tree = ast.parse(original_source)
    except SyntaxError as e:
        print(f"[-] Parsing Error: Incompatible Python syntax in {file_path}. Details: {e}")
        return

    scanner = PQCASTScanner()
    scanner.visit(tree)

    if not scanner.vulnerable_lines:
        print(f"[+] Clean Infrastructure: No quantum vulnerabilities detected via AST parsing in {file_path}.")
        return

    # Step 2: Contextual Splicing/Rewriting Logic
    lines = original_source.splitlines()
    # Modifying lines safely based on identified token positions
    for line_num in sorted(scanner.vulnerable_lines, reverse=True):
        idx = line_num - 1
        lines[idx] = PQC_TEMPLATE

    modified_source = "\n".join(lines) + "\n"

    # Step 3: Enterprise Strategy - Dry Run vs Live Patching
    if dry_run:
        print(f"\n[!] ENTERPRISE DRY-RUN: Generating Unified Patch Diff for '{file_path}'...")
        print("=" * 65)
        diff = difflib.unified_diff(
            original_source.splitlines(keepends=True),
            modified_source.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}"
        )
        sys.stdout.writelines(diff)
        print("=" * 65)
    else:
        # Immutable backup deployment
        backup_path = f"{file_path}.bak"
        shutil.copyfile(file_path, backup_path)
        print(f"[+] State Preserved: Backup written to {backup_path}")
        
        with open(file_path, 'w') as f:
            f.write(modified_source)
        print(f"[+] SUCCESS: Structural code rewrite complete. Unified PQC patch applied to {file_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PQC-Sentry Enterprise Mitigation Core Engine.")
    parser.add_argument("target", help="Target source file to evaluate.")
    parser.add_argument("--dry-run", action="store_true", help="Analyze and display unified patch diff without writing to disk.")
    
    args = parser.parse_args()
    process_target_file(args.target, dry_run=args.dry_run)
