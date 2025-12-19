#!/usr/bin/env python3
"""
Generate commit proof: RSA-PSS signature encrypted with instructor's public key
"""
import sys
import base64
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import STUDENT_PRIVATE_KEY, INSTRUCTOR_PUBLIC_KEY
from app.crypto.keys import load_private_key, load_public_key
from app.crypto.rsa_ops import sign_pss, encrypt_oaep


def get_commit_hash() -> str:
    """Get current commit hash"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit hash: {e}")
        sys.exit(1)


def generate_proof():
    """Generate commit proof"""
    print("Generating commit proof...\n")
    
    # Get commit hash
    commit_hash = get_commit_hash()
    print(f"Commit Hash: {commit_hash}")
    
    # Load keys
    print("\nLoading keys...")
    student_private_key = load_private_key(STUDENT_PRIVATE_KEY)
    instructor_public_key = load_public_key(INSTRUCTOR_PUBLIC_KEY)
    
    # Sign commit hash with student private key (RSA-PSS-SHA256)
    print("Signing commit hash with student private key (RSA-PSS-SHA256)...")
    signature = sign_pss(commit_hash, student_private_key)
    print(f"Signature length: {len(signature)} bytes")
    
    # Encrypt signature with instructor public key (RSA/OAEP-SHA256)
    print("Encrypting signature with instructor public key (RSA/OAEP-SHA256)...")
    encrypted_signature = encrypt_oaep(signature, instructor_public_key)
    print(f"Encrypted signature length: {len(encrypted_signature)} bytes")
    
    # Base64 encode
    encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode('utf-8')
    
    print("\n" + "="*80)
    print("COMMIT PROOF GENERATED SUCCESSFULLY")
    print("="*80)
    print(f"\nCommit Hash:\n{commit_hash}")
    print(f"\nEncrypted Commit Signature (Base64):\n{encrypted_signature_b64}")
    print("\n" + "="*80)
    print("\nCopy the above values for submission.")
    print("IMPORTANT: The encrypted signature must be a SINGLE LINE with no breaks!")
    print("="*80)


if __name__ == "__main__":
    generate_proof()
