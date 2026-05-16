from options_tools import verify_account_capital, fetch_high_yield_chain

def pre_market_checklist():
    print("🔍 Pre-Market Health Check...")
    
    # Check 1: Account Capital
    try:
        capital = verify_account_capital()
        if capital > 0:
            print(f"✅ Account funded: ${capital}")
        else:
            print(f"⚠️  WARNING: No available capital!")
            return False
    except Exception as e:
        print(f"❌ Capital check failed: {e}")
        return False
    
    # Check 2: API Connectivity (test with a major ticker)
    try:
        result = fetch_high_yield_chain("SPY")
        print(f"✅ Options chain accessible")
        print(f"   Sample data: {result[:100]}...")
    except Exception as e:
        print(f"❌ Options chain error: {e}")
        return False
    
    print("\n✅ All systems ready for market open!\n")
    return True

if __name__ == "__main__":
    pre_market_checklist()
