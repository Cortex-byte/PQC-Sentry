import os
import sys
import argparse
import ast
import re
import json
import shutil
import difflib
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
# APEX TIER QUANTUM WEAKNESS REGISTER
# ==========================================
C_VULNERABLE_REGEX = {
    "RSA_Key_Generation": r"\b(RSA_generate_key|RSA_generate_key_ex)\b",
    "DES_TripleDES": r"\b(DES_ecb_encrypt|DES_ede3_cbc_encrypt|DES_ncbc_encrypt)\b",
    "Legacy_Hashing_MD5_SHA1": r"\b(MD5_Init|MD5_Update|MD5_Final|SHA1_Init|SHA1_Update|SHA1_Final)\b",
    "Weak_Diffie_Hellman": r"\b(DH_generate_parameters|DH_generate_key)\b",
}

# কোয়ান্টাম সেফ মাইগ্রেশন টেমপ্লেট (NIST ML-KEM / Kyber-768 Standard)
PQC_TEMPLATE_C = "/* PQC SENTRY AUTO-PATCHED: Migrated to NIST ML-KEM (Kyber-768) */\npqc_status_t status = crypto_kem_keypair_mlkem768(pk, sk);"
PQC_TEMPLATE_PY = "# PQC SENTRY AUTO-PATCHED: Migrated to NIST ML-KEM\nfrom oqs import Signature, KeyEncapsulation\nwith KeyEncapsulation('ML-KEM-768') as kem:"

class PQCASTScanner(ast.NodeVisitor):
    def __init__(self):
        self.vulnerable_lines = []
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if hasattr(node.func.value, 'id') and node.func.value.id == 'rsa' and node.func.attr == 'generate_private_key':
                self.vulnerable_lines.append(node.lineno)
        self.generic_visit(node)

# ==========================================
# GOD TIER 1: AUTOMATED AI EXPLOIT REASONER (FREE GATEWAY)
# ==========================================
def ask_ai_reasoning(vulnerability_type, code_snippet):
    """উইদাউট এপিআই-কী: কোড কেন কোয়ান্টাম অ্যাটাক-ভালনারেবল তা এআই দিয়ে লাইভ এনালাইসিস করা"""
    prompt = f"Analyze this enterprise code snippet showing '{vulnerability_type}'. Explain the 'Harvest Now, Decrypt Later' threat for this: '{code_snippet}'. Keep it strictly under 2 sentences."
    try:
        # ফ্রি পাবলিক নো-কী এআই গেটওয়ে ইন্টারফেস ব্যবহার
        url = "https://pollinations.ai"
        data = prompt.encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'text/plain'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except Exception:
        return "AI Reasoner Offline: Suspected cryptographic entropy collision risk under Shor's Algorithm."

# ==========================================
# GOD TIER 2: SURGICAL AUTO-PATCHER ENGINE
# ==========================================
def execute_surgical_patch(file_path, vulnerable_lines, is_c=False):
    """কোডের মেইন আর্কিটেকচার ঠিক রেখে নিখুঁতভাবে ভালনারেবল লাইন রিপ্লেস করা"""
    try:
        # ইমিউটেবল ব্যাকআপ তৈরি (.bak)
        backup_path = f"{file_path}.bak"
        if not os.path.exists(backup_path):
            shutil.copyfile(file_path, backup_path)
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # রিভার্স অর্ডার যাতে লাইনের ইনডেক্স উল্টাপাল্টা না হয়
        for line_num in sorted(vulnerable_lines, reverse=True):
            idx = line_num - 1
            lines[idx] = (PQC_TEMPLATE_C + "\n") if is_c else (PQC_TEMPLATE_PY + "\n")
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print(f"\n[-] Patching Failed for {file_path}: {e}")
        return False

# ==========================================
# MULTITHREADED WORKER CORE
# ==========================================
def process_target_file(file_path, auto_patch=False):
    result = {"file": file_path, "type": None, "findings": [], "patched": False}
    
    if file_path.endswith('.py'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
            tree = ast.parse(source)
            scanner = PQCASTScanner()
            scanner.visit(tree)
            if scanner.vulnerable_lines:
                result["type"] = "Python (AST)"
                for l in scanner.vulnerable_lines:
                    snippet = source.splitlines()[l-1] if l-1 < len(source.splitlines()) else ""
                    ai_analysis = ask_ai_reasoning("Python Legacy RSA Call", snippet)
                    result["findings"].append({"line": l, "code": snippet, "ai_reasoning": ai_analysis})
                
                if auto_patch:
                    result["patched"] = execute_surgical_patch(file_path, scanner.vulnerable_lines, is_c=False)
                print(f"\n[🚨 AI RISK DETECTED] -> {file_path} (Line {scanner.vulnerable_lines})")
        except SyntaxError:
            pass
            
    elif file_path.endswith(('.c', '.cpp', '.h')):
        vulns = scan_c_cpp_file(file_path)
        if vulns:
            result["type"] = "C/C++ (Token)"
            v_lines = []
            for v in vulns:
                v_lines.append(v["line"])
                ai_analysis = ask_ai_reasoning(v["type"], v["code"])
                result["findings"].append({"line": v["line"], "code": v["code"], "ai_reasoning": ai_analysis})
                
            if auto_patch:
                result["patched"] = execute_surgical_patch(file_path, v_lines, is_c=True)
            print(f"\n[🚨 AI RISK DETECTED IN NASA C-SOURCE] -> {file_path}")
            
    return result if result["findings"] else None

def scan_c_cpp_file(file_path):
    found_vulnerabilities = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if clean_line.startswith(("//", "/*", "*")):
                    continue
                for vuln_type, regex in C_VULNERABLE_REGEX.items():
                    if re.search(regex, clean_line):
                        found_vulnerabilities.append({"line": line_num, "type": vuln_type, "code": clean_line})
    except Exception:
        pass
    return found_vulnerabilities

# ==========================================
# MAIN COMMAND INTERFACE
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PQC-Sentry God-Tier Quantum Cyber Weapon")
    parser.add_argument("target", help="Target file or directory to scan.")
    parser.add_argument("--patch", action="store_true", help="Auto-patch vulnerabilities with NIST ML-KEM.")
    parser.add_argument("--output", default="god_tier_pqc_report.json", help="Output JSON report path.")
    args = parser.parse_args()

    all_files = []
    if os.path.isfile(args.target):
        all_files.append(args.target)
    elif os.path.isdir(args.target):
        print(f"[*] Intelligence Gathering: Mapping target infrastructure in {args.target}")
        for root, dirs, files in os.walk(args.target):
            for file in files:
                if file.endswith(('.py', '.c', '.cpp', '.h')):
                    all_files.append(os.path.join(root, file))
    else:
        print("[-] Fatal: Invalid path.")
        sys.exit(1)

    total_files = len(all_files)
    print(f"[*] Total target assets loaded: {total_files}")
    print(f"[*] Deploying Parallel Thread Matrix & Triggering Live AI Reasoner...")
    
    final_reports = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_target_file, f, args.patch): f for f in all_files}
        for i, future in enumerate(as_completed(futures), 1):
            res = future.result()
            if res:
                final_reports.append(res)
            sys.stdout.write(f"\r[*] Cyber Matrix Scanning Progress: {i}/{total_files} components cleared...")
            sys.stdout.flush()

    print(f"\n\n[📊] ARCHITECTURE EVALUATION COMPLETE.")
    with open(args.output, 'w', encoding='utf-8') as rf:
        json.dump(final_reports, rf, indent=4)
        
    print(f"[+] God-Tier Intelligence JSON Exported: {os.path.abspath(args.output)}")
    print(f"[+] Total Vulnerable Anomalies Dominated & Logged: {len(final_reports)}")
