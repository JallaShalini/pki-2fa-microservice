import pytest
from app.crypto.rsa_ops import decrypt_seed, sign_message, encrypt_message
from app.crypto.keys import load_private_key, load_public_key

def test_decrypt_seed():
    """Test RSA-OAEP decryption"""
    private_key = load_private_key("student_private.pem")
    # Test with sample encrypted data
    encrypted = b"sample_encrypted_data"
    # Add actual decryption test
    
def test_sign_message():
    """Test RSA-PSS signing"""
    private_key = load_private_key("student_private.pem")
    message = b"test message"
    signature = sign_message(private_key, message)
    assert len(signature) > 0
    
def test_encrypt_message():
    """Test RSA-OAEP encryption"""
    public_key = load_public_key("instructor_public.pem")
    message = b"test seed"
    encrypted = encrypt_message(public_key, message)
    assert len(encrypted) > 0

def test_key_loading():
    """Test loading RSA keys from PEM files"""
    private_key = load_private_key("student_private.pem")
    public_key = load_public_key("student_public.pem")
    assert private_key is not None
    assert public_key is not None
