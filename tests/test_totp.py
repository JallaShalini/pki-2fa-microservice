import pytest
from app.totp.totp_service import generate_totp_code, verify_totp_code, hex_to_base32, get_remaining_validity

def test_generate_totp_code():
    """Test TOTP code generation"""
    hex_seed = "48656c6c6f20576f726c64"  # "Hello World" in hex
    code = generate_totp_code(hex_seed)
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()

def test_verify_totp_code():
    """Test TOTP verification with valid code"""
    hex_seed = "48656c6c6f20576f726c64"
    code = generate_totp_code(hex_seed)
    assert verify_totp_code(hex_seed, code) is True

def test_verify_invalid_code():
    """Test TOTP verification with invalid code"""
    hex_seed = "48656c6c6f20576f726c64"
    invalid_code = "000000"
    assert verify_totp_code(hex_seed, invalid_code) is False

def test_hex_to_base32():
    """Test hex to base32 conversion"""
    hex_seed = "48656c6c6f20576f726c64"
    base32 = hex_to_base32(hex_seed)
    assert base32 is not None
    assert len(base32) > 0

def test_get_remaining_validity():
    """Test getting remaining validity"""
    remaining = get_remaining_validity(30)
    assert remaining >= 0
    assert remaining <= 30
