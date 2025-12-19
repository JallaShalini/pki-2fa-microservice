"""
Configuration settings for the application
"""
import os
from pathlib import Path

# Timezone
TIMEZONE = os.getenv("TZ", "UTC")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path("/data")
CRON_DIR = Path("/cron")
SEED_FILE = DATA_DIR / "seed.txt"

# Key files
STUDENT_PRIVATE_KEY = BASE_DIR / "student_private.pem"
STUDENT_PUBLIC_KEY = BASE_DIR / "student_public.pem"
INSTRUCTOR_PUBLIC_KEY = BASE_DIR / "instructor_public.pem"

# Server settings
HOST = "0.0.0.0"
PORT = 8080
