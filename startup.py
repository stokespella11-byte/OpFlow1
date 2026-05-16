#!/usr/bin/env python3
"""
OpFlow1 Pre-Market Startup Script
Runs all necessary health checks before market opening.
"""

import sys
from dotenv import load_dotenv
from test_connection import verify_account_capital
from market_check import market_status
from trading_logger import logger

load_dotenv()

def startup_sequence():
    """Execute complete startup sequence."""
    print("\n" + "="*50)
    print("OpFlow1 - Pre-Market Startup Sequence")
    print("="*50 + "\n")
    
    checks_passed = 0
    checks_total = 3
    
    # Check 1: Market Status
    print("1️⃣  Checking market status...")
    if market_status():
        print("   ✅ Market is open\n")
        checks_passed += 1
    else:
        print("   ⚠️  Market is closed (non-critical)\n")
    
    # Check 2: API Connection
    print("2️⃣  Testing API connection...")
    try:
        capital = verify_account_capital()
        if capital > 0:
            print(f"   ✅ Connected! Capital: ${capital}\n")
            checks_passed += 1
        else:
            print(f"   ❌ No available capital\n")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}\n")
    
    # Check 3: Environment Variables
    print("3️⃣  Verifying environment configuration...")
    try:
        import os
        secret = os.getenv("PUBLIC_COM_SECRET")
        account = os.getenv("PUBLIC_COM_ACCOUNT_ID")
        
        if secret and account:
            print("   ✅ API credentials configured\n")
            checks_passed += 1
        else:
            print("   ❌ Missing API credentials in .env\n")
    except Exception as e:
        print(f"   ❌ Configuration check failed: {e}\n")
    
    # Summary
    print("="*50)
    print(f"Startup Status: {checks_passed}/{checks_total} checks passed")
    print("="*50 + "\n")
    
    if checks_passed >= 2:
        logger.info("Startup sequence completed successfully")
        print("✅ OpFlow1 is READY for trading!\n")
        return True
    else:
        logger.error("Startup sequence failed - resolve errors before trading")
        print("❌ Please resolve errors before trading\n")
        return False

if __name__ == "__main__":
    success = startup_sequence()
    sys.exit(0 if success else 1)
