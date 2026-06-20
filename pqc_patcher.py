import os
import sys
import argparse
import ast
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
# ENTERPRISE QUANTUM RISK SIGNATURES (C/C++)
# ==========================================
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
        if isinstance(node.func, ast.Attribute):
            if hasattr(node.func.value, 'id') and node.func.value.id == 'rsa' and node.func.attr == 'generate_private_key':
                self.vulnerable_lines.append(node.lineno)
        self.generic_visit(node)

def scan_c_cpp_file(file_path):
    """Scans legacy C/C++ source and header files using optimized regex tokens."""
    found_vulnerabilities = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if clean_line.startswith(("//", "/*", "*")):
                    continue
                for vuln_type, regex in C_VULNERABLE_REGEX.items():
                    if re.search(regex, clean_line):
                        found_vulnerabilities.append({
                            "line": line_num,
                            "type": vuln_type,
                            "code": clean_line
                        })
    except Exception:
        pass
    return found_vulnerabilities

# ==========================================
# PARALLEL EXECUTION WORKER
# ==========================================
def process_target_file(file_path):
    """Worker function optimized for thread execution."""
    result = {"file": file_path, "type": None, "findings": []}
    
    if file_path.endswith('.py'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
            tree = ast.parse(source)
            scanner = PQCASTScanner()
            scanner.visit(tree)
            if scanner.vulnerable_lines:
                result["type"] = "Python (AST)"
                result["findings"] = [{"line": l, "type": "Quantum Cryptography Call"} for l in scanner.vulnerable_lines]
                print(f"[🚨] AST RISK FOUND -> {file_path}")
        except SyntaxError:
            pass
            
    elif file_path.endswith(('.c', '.cpp', '.h')):
        vulns = scan_c_cpp_file(file_path)
        if vulns:
            result["type"] = "C/C++ (Token)"
            result["findings"] = vulns
            print(f"[🚨] CRYPTO RISK FOUND IN C-SOURCE -> {file_path}")
            
    return result if result["findings"] else None

# ==========================================
# MAIN INTERFACE WITH MULTITHREADING
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PQC-Sentry Apex Tier Multithreaded Migration Engine")
    parser.add_argument("target", help="Target source file or directory to evaluate.")
    parser.add_argument("--output", default="pqc_vulnerability_report.json", help="Output JSON report name.")
    args = parser.parse_args()

    all_files = []
    if os.path.isfile(args.target):
        all_files.append(args.target)
    elif os.path.isdir(args.target):
        print(f"[*] Mapping infrastructure files in: {args.target}")
        for root, dirs, files in os.walk(args.target):
            for file in files:
                if file.endswith(('.py', '.c', '.cpp', '.h')):
                    all_files.append(os.path.join(root, file))
    else:
        print("[-] Error: Invalid target path.")
        sys.exit(1)

    total_files = len(all_files)
    print(f"[*] Total valid target assets discovered: {total_files}")
    print(f"[*] Initializing Apex Core Multi-threading (Parallel Workers)...")
    
    final_reports = []
    
    # ThreadPoolExecutor ব্যবহার করে আপনার পিসির সব কোর একসাথে একটিভ করা হলো
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_target_file, f): f for f in all_files}
        for i, future in enumerate(as_completed(futures), 1):
            res = future.result()
            if res:
                final_reports.append(res)
            # লাইভ প্রোগ্রেস বার (রিয়েল হ্যাকিং টুলের ফিল পাওয়ার জন্য)
            sys.stdout.write(f"\r[*] Progress: {i}/{total_files} assets evaluated...")
            sys.stdout.flush()

    # JSON ফাইলে এক্সপোর্ট লজিক
    print(f"\n\n[📊] SCAN COMPLETE. Exporting structural JSON data...")
    with open(args.output, 'w', encoding='utf-8') as report_file:
        json.dump(final_reports, report_file, indent=4)
        
    print(f"[+] Elite Report Saved Successfully -> {os.path.abspath(args.output)}")
    print(f"[+] Total Vulnerable Structural Anomalies Detected: {len(final_reports)}")
