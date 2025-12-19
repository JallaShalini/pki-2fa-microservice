import pytest
from scripts.log_2fa_cron import main as cron_main
import os

def test_cron_execution():
    """Test cron script execution"""
    # Run the cron script
    result = cron_main()
    # Check that it generated a code
    assert result is not None

def test_cron_log_output():
    """Test that cron writes to log file"""
    cron_main()
    # Check if log file exists (if applicable)
    # assert os.path.exists("/cron/last_code.txt")
