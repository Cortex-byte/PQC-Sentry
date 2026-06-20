import os
import sys
import argparse
import ast
import re

# ==========================================
# PHASE 1 & 2: QUANTUM VULNERABILITY SIGNATURES (C/C++)
# ==========================================
# নাসার C কোডে ব্যবহৃত সম্ভাব্য সব কোয়ান্টাম-দুর্বল ফাংশন এবং ক্রিপ্টো অ্যালগরিদম
C_VULNERABLE_REGEX = {
    "RSA_Key_Generation": r"\b(RSA_generate_key|RSA_generate_key_ex)\b",
    "DES_TripleDES": r"\b(DES_ecb_encrypt|DES_ede3_cbc_encrypt|DES_ncbc_encrypt)\b",
    "Legacy_Hashing_MD5_SHA1": r"\b(MD5_Init|MD5_Update|MD5_Final|SHA1_Init|SHA1_Update|SHA1_Final)\b",
    "Weak_Diffie_Hellman": r"\b(DH_generate_parameters|DH_generate_key)\b",
    "Hardcoded_Crypto_Key": r"\b(AES_KEY|secret_key|private_key|auth_token)\s*=\s*[\"'][a-zA-Z0-9+/=]{8,}[\"']"
}

class PQCASTScanner(ast.NodeVisitor):
    """AST Visitor for Python files to pinpoint quantum-vulnerable functions structurally."""
    def __init__(self):
        self.vulnerable_lines = []

    def visit_Call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            if hasattr(node.func.value, 'id') and node.func.value.id == 'rsa' and node.func.attr == 'generate_private_key':
                func_name = "rsa.generate_private_key"
        
        if func_name:
            self.vulnerable_lines.append(node.lineno)
        self.generic_visit(node)

# ==========================================
# C/C++ SCANNING ENGINE (NEW FEATURE FOR NASA/SPACEX)
# ==========================================
def scan_c_cpp_file(file_path):
    """Scans legacy C/C++ source and header files using optimized regex tokens."""
    found_vulnerabilities = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                # কমেন্ট লাইন বাদ দেওয়া (False Positives কমানোর জন্য)
                if clean_line.startswith("//") or clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                
                for vuln_type, regex in C_VULNERABLE_REGEX.items():
                    if re.search(regex, clean_line):
                        found_vulnerabilities.append({
                            "line": line_num,
                            "type": vuln_type,
                            "code": clean_line
                        })
    except Exception as e:
        print(f"[-] Error reading C file {file_path}: {e}")
    return found_vulnerabilities

# ==========================================
# CORE PROCESSOR ENGINE
# ==========================================
def process_target_file(file_path, dry_run=False):
    # পাইথন ফাইলের জন্য AST পার্সিং
    if file_path.endswith('.py'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_source = f.read()
            tree = ast.parse(original_source)
            scanner = PQCASTScanner()
            scanner.visit(tree)
            
            if not scanner.vulnerable_lines:
                print(f"[+] Clean (Python AST): {file_path}")
                return
            
            print(f"[!] VULNERABILITY DETECTED in Python File: {file_path} at lines {scanner.vulnerable_lines}")
            # এখানে আপনার আগের অটো-প্যাচিং/রাইটিং লজিক কাজ করবে...
        except SyntaxError:
            print(f"[-] Parsing Error: Incompatible Python syntax in {file_path}")
            
    # C/C++ ফাইলের জন্য টোকেন এবং রিজেক্স স্ক্যানিং (নাসার জন্য স্পেশাল)
    elif file_path.endswith(('.c', '.cpp', '.h')):
        vulns = scan_c_cpp_file(file_path)
        if not vulns:
            # কমেন্ট আউট করে রাখতে পারেন যাতে টার্মিনালে ক্লিন ফাইলের ভিড় না হয়
            # print(f"[+] Clean (C/C++ Token): {file_path}")
            return
        
        print(f"\n[🚨] QUANTUM RISK FOUND IN NASA C-SOURCE: {file_path}")
        for v in vulns:
            print(f"    ↳ Line {v['line']}: [{v['type']}] -> {v['code']}")

# ==========================================
# MAIN EXECUTION INTERFACE
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PQC-Sentry Enterprise Mitigation Core Engine V2")
    parser.add_argument("target", help="Target source file or directory to evaluate.")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without modifying disk.")
    args = parser.parse_args()

    if os.path.isfile(args.target):
        process_target_file(args.target, dry_run=args.dry_run)
        
    elif os.path.isdir(args.target):
        print(f"[*] Starting PQC-Sentry Recursive Scan on: {args.target}")
        py_count = 0
        c_count = 0
        
        for root, dirs, files in os.walk(args.target):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith('.py'):
                    py_count += 1
                    process_target_file(full_path, dry_run=args.dry_run)
                elif file.endswith(('.c', '.cpp', '.h')):
                    c_count += 1
                    process_target_file(full_path, dry_run=args.dry_run)
                    
        print(f"\n[📊] SCAN SUMMARY:")
        print(f"    ↳ Total Python Files Analyzed: {py_count}")
        print(f"    ↳ Total C/C++ Assets Analyzed: {c_count}")
        print(f"    ↳ Quantum Risk Status: Evaluation Complete.")
    else:
        print("[-] Error: Invalid target path.")

    parser = argparse.ArgumentParser(description="PQC-Sentry Enterprise Mitigation Core Engine V2")
    parser.add_init = parser.add_argument("target", help="Target source file or directory to evaluate.")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without modifying disk.")
    args = parser.parse_args()

    if os.path.isfile(args.target):
        process_target_file(args.target, dry_run=args.dry_run)
        
    elif os.path.isdir(args.target):
        print(f"[*] Starting PQC-Sentry Recursive Scan on: {args.target}")
        for root, dirs, files in os.walk(args.target):
            for file in files:
                if file.endswith(('.py', '.c', '.cpp', '.h')):
                    full_path = os.path.join(root, file)
                    process_target_file(full_path, dry_run=args.dry_run)
    else:
        print("[-] Error: Invalid target path.")
