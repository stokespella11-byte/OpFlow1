"""OpFlow Main Entry Point

Executable script to run OpFlow trading tools.
"""

import os
from dotenv import load_dotenv
from opflow.tools import verify_account_capital, fetch_high_yield_chain

# Load environment variables from .env file
load_dotenv()


def main():
    """Run the OpFlow trading workflow."""
    
    print("="*60)
    print("OpFlow - Options Trading Automation")
    print("="*60)
    print()
    
    # Verify credentials are set
    if not os.getenv("PUBLIC_COM_SECRET") or not os.getenv("PUBLIC_COM_ACCOUNT_ID"):
        print("❌ Error: API credentials not found in .env file")
        print("   Please copy .env.example to .env and add your credentials")
        return
    
    # Step 1: Verify account capital
    print("[1] Checking account capital...")
    try:
        capital = verify_account_capital()
        print(f"    ✓ Available capital: ${capital:,.2f}")
    except Exception as e:
        print(f"    ✗ Error checking capital: {str(e)}")
        return
    
    print()
    
    # Step 2: Scan for opportunities
    print("[2] Scanning options chains for high-yield spreads...")
    tickers = ["SPY", "QQQ", "IWM"]
    
    for ticker in tickers:
        print(f"\n    Scanning {ticker}...")
        try:
            result = fetch_high_yield_chain(ticker)
            print(f"    {result}")
        except Exception as e:
            print(f"    Error scanning {ticker}: {str(e)}")
    
    print()
    print("="*60)
    print("OpFlow scan complete!")
    print("="*60)
    print()
    print("Next steps:")
    print("  - Review opportunities above")
    print("  - Uncomment execute_bull_put_spread() in main.py to enable live trading")
    print("  - Always test with paper trading first")
    print()


if __name__ == "__main__":
    main()
