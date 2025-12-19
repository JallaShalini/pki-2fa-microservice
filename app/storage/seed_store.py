"""
Seed storage operations
"""
from pathlib import Path
from app.logging_config import logger


def save_seed(seed: str, seed_file: Path) -> None:
    """
    Save seed to persistent storage
    
    Args:
        seed: Hex seed string to save
        seed_file: Path to seed file
    """
    # Ensure directory exists
    seed_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write seed to file
    with open(seed_file, 'w') as f:
        f.write(seed.strip())
    
    logger.info(f"Seed saved to {seed_file}")


def load_seed(seed_file: Path) -> str:
    """
    Load seed from persistent storage
    
    Args:
        seed_file: Path to seed file
        
    Returns:
        Hex seed string
        
    Raises:
        FileNotFoundError: If seed file doesn't exist
    """
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_file}")
    
    with open(seed_file, 'r') as f:
        seed = f.read().strip()
    
    return seed


def seed_exists(seed_file: Path) -> bool:
    """
    Check if seed file exists
    
    Args:
        seed_file: Path to seed file
        
    Returns:
        True if seed file exists, False otherwise
    """
    return seed_file.exists()
