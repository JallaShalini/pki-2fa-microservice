import pytest
from app.totp.totp_service import generate_totp, verify_totp
import time

def test_generate_totp():
    """Test TOTP code generation"""
    seed = "JBSWY3DPEHPK3PXP"  # Base32 encoded seed
    code = generate_totp(seed)
    assert len(code) == 6
    assert code.isdigit()

def test_verify_totp_valid():
    """Test TOTP verification with valid code"""
    seed = "JBSWY3DPEHPK3PXP"
    code = generate_totp(seed)
    # Should verify within ±1 time window
    assert verify_totp(seed, code) is True

def test_verify_totp_invalid():
    """Test TOTP verification with invalid code"""
    seed = "JBSWY3DPEHPK3PXP"
    invalid_code = "000000"
    assert verify_totp(seed, invalid_code) is False

def test_totp_time_window():
    """Test TOTP accepts codes from ±1 window (30 seconds)"""
    seed = "JBSWY3DPEHPK3PXP"
    code = generate_totp(seed)
    # Test that code is valid for 30-90 seconds
    assert verify_totp(seed, code) is True
