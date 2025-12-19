#!/usr/bin/env python3
"""
Cron script to log 2FA codes every minute
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import SEED_FILE
from app.totp.totp_service import generate_totp_code


def main():
    """Generate and log current TOTP code"""
    try:
        # Check if seed file exists
        if not SEED_FILE.exists():
            print("Error: Seed file not found", file=sys.stderr)
            sys.exit(1)
        
        # Read seed
        with open(SEED_FILE, 'r') as f:
            hex_seed = f.read().strip()
        
        # Generate TOTP code
        code = generate_totp_code(hex_seed)
        
        # Get current UTC timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print formatted output
        print(f"{timestamp} - 2FA Code: {code}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
