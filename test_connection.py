#!/usr/bin/env python3
"""
Test API Connection to Public.com
Verifies credentials and account access before market trading.
"""

import os
from dotenv import load_dotenv
from options_tools import verify_account_capital as get_capital
from trading_logger import logger, log_success, log_error

load_dotenv()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("OpFlow1 - API Connection Test")
    print("="*50 + "\n")
    
    # Check environment variables
    print("1️⃣  Checking environment configuration...")
    secret = os.getenv("PUBLIC_COM_SECRET")
    account = os.getenv("PUBLIC_COM_ACCOUNT_ID")
    
    if not secret or not account:
        log_error("Missing API credentials in .env file")
        print("   Please configure .env with:")
        print("   - PUBLIC_COM_SECRET")
        print("   - PUBLIC_COM_ACCOUNT_ID\n")
        exit(1)
    
    print("   ✅ Environment variables loaded\n")
    
    # Test connection
    print("2️⃣  Testing Public.com API connection...")
    try:
        capital = get_capital()
        log_success(f"Connected to Public.com! Available Capital: ${capital}")
        print(f"   Capital: ${capital}\n")
        
        print("="*50)
        print("✅ Connection Test PASSED")
        print("="*50 + "\n")
        exit(0)
        
    except Exception as e:
        log_error(f"API Connection Failed: {str(e)}")
        print(f"   Error: {str(e)}\n")
        
        print("="*50)
        print("❌ Connection Test FAILED")
        print("="*50)
        print("\nTroubleshooting:")
        print("- Verify API credentials are correct in .env")
        print("- Check Public.com account status")
        print("- Ensure API access is enabled\n")
        exit(1)
