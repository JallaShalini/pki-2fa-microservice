import pytest
from app.crypto.rsa_ops import decrypt_oaep, sign_pss, encrypt_oaep
from app.crypto.keys import load_private_key, load_public_key

def test_load_private_key():
    """Test loading student private key"""
    private_key = load_private_key("student_private.pem")
    assert private_key is not None

def test_load_public_key():
    """Test loading student public key"""
    public_key = load_public_key("student_public.pem")
    assert public_key is not None

def test_load_instructor_public_key():
    """Test loading instructor public key"""
    instructor_key = load_public_key("instructor_public.pem")
    assert instructor_key is not None

def test_encrypt_oaep():
    """Test RSA-OAEP encryption"""
    public_key = load_public_key("instructor_public.pem")
    data = b"test message"
    encrypted = encrypt_oaep(data, public_key)
    assert encrypted is not None
    assert len(encrypted) > 0

def test_sign_pss():
    """Test RSA-PSS signing"""
    private_key = load_private_key("student_private.pem")
    message = "test message"
    signature = sign_pss(message, private_key)
    assert signature is not None
    assert len(signature) > 0
