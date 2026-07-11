#!/usr/bin/env python3
"""Encrypt questions.json using Fernet with password-derived key.

Usage:
    python scripts/encrypt_questions.py

Requires:
    pip install cryptography
"""

import hashlib
import base64
from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("cryptography not installed. Run: pip install cryptography")
    import sys
    sys.exit(1)

PASSWORD = "songjoo"


def main():
    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "questions.json"
    output_path = base_dir / "data" / "questions.enc"

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return

    data = input_path.read_bytes()

    key = base64.urlsafe_b64encode(hashlib.sha256(PASSWORD.encode()).digest())
    f = Fernet(key)
    token = f.encrypt(data)

    output_path.write_text(token.decode("utf-8"), encoding="utf-8")
    print(f"Encrypted {len(data)} bytes -> {output_path}")


if __name__ == "__main__":
    main()
