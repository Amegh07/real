"""
Automated Code Audit Pipeline v2
=============================
Enhanced multi-pass auditing.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "backend" / ".env")
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from groq_client.groq_client import GroqClient

CHUNK_SIZE = 100

PASSES = [
    ("Bugs", "Find syntax errors, NameError, TypeError, AttributeError, uninitialized variables"),
    ("Logic", "Find logic flaws, wrong conditions, incorrect operators, off-by-one errors"),
    ("Edge", "Find edge cases: empty list, None access, division by zero, index out of range"),
    ("Perf", "Find performance issues: N+1, nested loops, inefficient lookups"),
    ("Security", "Find security: hardcoded secrets, injection, eval(), unsafe yaml load"),
    ("Design", "Find design: bare except, no error handling, god classes, tight coupling"),
    ("Break", "What inputs or states would crash this code?"),
    ("Verdict", "Rate safety 1-10. What MUST be fixed?")
]


def chunk_code(code, size):
    lines = code.split("\n")
    return ["\n".join(lines[i:i+size]) for i in range(0, len(lines), size)]


def run_pass(client, code, file_name, pass_num, pass_name, pass_desc):
    prompt = f"""Review ONLY this chunk of {file_name}.

PASS {pass_num}: {pass_name}
{pass_desc}

Report issues FOUND. Format:
- issue at line X: description

If no issues: "NONE"

<code>
{code}
</code>"""
    try:
        return client.complete(prompt)
    except:
        return "ERROR"


def audit_file(client, full_path):
    base_name = Path(full_path).name

    with open(full_path, "r", encoding="utf-8") as f:
        code = f.read()

    chunks = chunk_code(code, CHUNK_SIZE)
    issues = []

    for i, chunk in enumerate(chunks):
        chunk_id = f"{i+1}/{len(chunks)}"
        print(f"  [{chunk_id}]", end=" ", flush=True)

        chunk_issues = []
        for pnum, (pname, pdesc) in enumerate(PASSES, 1):
            result = run_pass(client, chunk, base_name, pnum, pname, pdesc)
            if result and "NONE" not in result and "ERROR" not in result:
                chunk_issues.append(f"{pname}: {result.strip()}")

        if chunk_issues:
            issues.extend(chunk_issues)
            print(f"({len(chunk_issues)})")
        else:
            print("OK")

    return issues


def run_pipeline(folder):
    api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        print("[!] No API key")
        return

    config = {"groq_api_key": api_key}
    client = GroqClient(config)

    if not client.enabled:
        print("[!] Client not enabled")
        return

    print(f"Auditing: {folder}\n")

    # Get all files
    files = []
    path = Path(folder)
    if path.is_file():
        files = [str(path)]
    else:
        files = [str(f) for f in path.rglob("*.py") if "test_" not in f.name and "__pycache__" not in str(f)]

    total_issues = []

    for f in files:
        rel = str(Path(f).relative_to(Path(folder).parent))
        print(f"\n[{rel}]")

        issues = audit_file(client, f)
        total_issues.append(f"## {rel}\n" + "\n".join(issues) if issues else f"## {rel}\nNO ISSUES")

    # Final analysis
    print("\n" + "="*60)
    print("FINAL ANALYSIS")
    print("="*60 + "\n")

    prompt = f"""Analyze ALL findings. Output JSON:

{{
  "critical_bugs": ["list MUST-FIX bugs"],
  "file_issues": {{"filename": "issue"}},
  "safety_score": 1-10,
  "immediate_fixes": ["what to fix first"]
}}

ALL FINDINGS:
{chr(10).join(total_issues)}"""

    result = client.complete(prompt)
    print(result)


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "backend/agents"
    run_pipeline(folder)