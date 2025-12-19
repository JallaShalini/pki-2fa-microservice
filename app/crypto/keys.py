"""
RSA key loading utilities
"""
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def load_private_key(key_path: Path):
    """
    Load RSA private key from PEM file
    
    Args:
        key_path: Path to the private key file
        
    Returns:
        RSA private key object
    """
    with open(key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def load_public_key(key_path: Path):
    """
    Load RSA public key from PEM file
    
    Args:
        key_path: Path to the public key file
        
    Returns:
        RSA public key object
    """
    with open(key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key
