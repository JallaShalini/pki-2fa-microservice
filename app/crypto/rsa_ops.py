"""
RSA cryptographic operations: OAEP decrypt, PSS sign, OAEP encrypt
"""
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_oaep(encrypted_data_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded data using RSA/OAEP with SHA-256
    
    Args:
        encrypted_data_b64: Base64-encoded ciphertext
        private_key: RSA private key object
        
    Returns:
        Decrypted plaintext string
    """
    # Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_data_b64)
    
    # RSA/OAEP decrypt with SHA-256 and MGF1
    plaintext_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Decode to string
    return plaintext_bytes.decode('utf-8')


def sign_pss(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256
    
    Args:
        message: Message string to sign (e.g., commit hash)
        private_key: RSA private key object
        
    Returns:
        Signature bytes
    """
    message_bytes = message.encode('utf-8')
    
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return signature


def encrypt_oaep(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA/OAEP with SHA-256
    
    Args:
        data: Data bytes to encrypt
        public_key: RSA public key object
        
    Returns:
        Encrypted ciphertext bytes
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return ciphertext
