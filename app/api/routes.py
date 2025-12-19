"""
API route handlers
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.api.models import (
    DecryptSeedRequest, DecryptSeedResponse,
    GenerateTOTPResponse, VerifyTOTPRequest, VerifyTOTPResponse,
    ErrorResponse, HealthResponse
)
from app.config import SEED_FILE, STUDENT_PRIVATE_KEY
from app.crypto.keys import load_private_key
from app.crypto.rsa_ops import decrypt_oaep
from app.totp.totp_service import generate_totp_code, get_remaining_validity, verify_totp_code
from app.storage.seed_store import save_seed, load_seed, seed_exists
from app.logging_config import logger

router = APIRouter()


@router.post("/decrypt-seed", response_model=DecryptSeedResponse, responses={500: {"model": ErrorResponse}})
async def decrypt_seed(request: DecryptSeedRequest):
    """
    Decrypt encrypted seed and store persistently
    """
    try:
        # Load student private key
        private_key = load_private_key(STUDENT_PRIVATE_KEY)
        
        # Decrypt seed
        hex_seed = decrypt_oaep(request.encrypted_seed, private_key)
        
        # Validate seed format (64-character hex)
        if len(hex_seed) != 64 or not all(c in '0123456789abcdef' for c in hex_seed.lower()):
            raise ValueError("Invalid seed format")
        
        # Save to persistent storage
        save_seed(hex_seed, SEED_FILE)
        
        logger.info("Seed decrypted and saved successfully")
        return DecryptSeedResponse(status="ok")
        
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Decryption failed"
        )


@router.get("/generate-2fa", response_model=GenerateTOTPResponse, responses={500: {"model": ErrorResponse}})
async def generate_2fa():
    """
    Generate current TOTP code
    """
    try:
        # Check if seed exists
        if not seed_exists(SEED_FILE):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Seed not decrypted yet"
            )
        
        # Load seed
        hex_seed = load_seed(SEED_FILE)
        
        # Generate TOTP code
        code = generate_totp_code(hex_seed)
        
        # Calculate remaining validity
        valid_for = get_remaining_validity()
        
        logger.info(f"Generated 2FA code: {code}")
        return GenerateTOTPResponse(code=code, valid_for=valid_for)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate 2FA code: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Seed not decrypted yet"
        )


@router.post("/verify-2fa", response_model=VerifyTOTPResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def verify_2fa(request
