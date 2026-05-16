import os
from dotenv import load_dotenv
from options_tools import verify_account_capital

load_dotenv()

# Test the connection
try:
    capital = verify_account_capital()
    print(f"✅ Connected! Available Capital: ${capital}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
