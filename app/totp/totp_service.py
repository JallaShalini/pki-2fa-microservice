"""
TOTP generation and verification service
"""
import base64
import time
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """
    Convert hex seed to base32 encoding for TOTP
    
    Args:
        hex_seed: 64-character hex string
        
    Returns:
        Base32-encoded seed string
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    
    Args:
        hex_seed: 64-character hex string
        
    Returns:
        6-digit TOTP code as string
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.now()


def get_remaining_validity(interval: int = 30) -> int:
    """
    Calculate remaining seconds in current TOTP period
    
    Args:
        interval: TOTP time period in seconds (default 30)
        
    Returns:
        Remaining seconds (0-29)
    """
    current_time = int(time.time())
    return interval - (current_time % interval)


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    
    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: Number of periods before/after to accept (default 1 = ±30s)
        
    Returns:
        True if code is valid, False otherwise
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.verify(code, valid_window=valid_window)
