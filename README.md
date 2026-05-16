import datetime
import numpy as np
import pandas as pd
import scipy.stats as si

# ==========================================
# CONSTANTS & CAPITAL CONFIGURATION
# ==========================================
STARTING_CAPITAL = 350.00
FRACTIONAL_MINIMUM = 5.00
TARGET_DIVIDEND_ETF = "JEPI"  # Options: JEPI, SCHD, etc.

# ==========================================
# STEP 1: BLACK-SCHOLES GREEKS CALCULATOR
# ==========================================
def calculate_option_delta(S, K, T, r, sigma, option_type='put'):
    """
    Calculates the Delta of a European Put or Call option.
    S: Stock price, K: Strike price, T: Time to expiration in years
    r: Risk-free interest rate, sigma: Implied Volatility (IV)
    """
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option_type == 'put':
        delta = si.norm.cdf(d1) - 1
    else:  # call
        delta = si.norm.cdf(d1)
    return round(delta, 2)

# ==========================================
# STEP 2: COVERED CALL CALCULATOR (NEW MODULE)
# ==========================================
def maximize_covered_call_expectations(cost_basis, current_stock_price, iv, days_to_expiry=14, r=0.04):
    """
    Evaluates different Call strikes to maximize the Total Profit Expectation.
    Total Expected Profit = Premium Received + Capital Appreciated (Strike - Cost Basis)
    Targeting a Call Delta between 0.25 and 0.35 (~70% probability of retaining shares).
    """
    S = current_stock_price
    T = days_to_expiry / 365.0
    
    # Generate realistic strike prices in $0.50 intervals around the stock price
    potential_strikes = [x for x in np.arange(0.5, S + 2.0, 0.5) if x >= S]
    
    best_strike = None
    max_expected_profit = -float('inf')
    best_delta = 0.0
    estimated_premium = 0.0
    
    for K in potential_strikes:
        delta = calculate_option_delta(S, K, T, r, iv, option_type='call')
        
        # Rule: Filter for Call Deltas around 0.30 to protect shares and maximize premium
        if 0.20 <= delta <= 0.40:
            # Estimate premium based on implied volatility and delta distance
            est_raw_premium = max(0.05, round((S * 0.06) * (iv / 0.5) * (1 - (delta - 0.3)), 2))
            
            # Capital Appreciation (Only realized if stock rises to or above the strike price)
            capital_gain_per_share = max(0, K - cost_basis)
            
            # Total upside potential package calculation
            total_potential_profit = (est_raw_premium + capital_gain_per_share) * 100
            
            # Identify the contract providing the peak absolute financial yield package
            if total_potential_profit > max_expected_profit:
                max_expected_profit = total_potential_profit
                best_strike = K
                best_delta = delta
                estimated_premium = est_raw_premium * 100

    if best_strike:
        return {
            'strike': best_strike,
            'delta': best_delta,
            'estimated_premium': estimated_premium,
            'capital_gain_potential': max(0, best_strike - cost_basis) * 100,
            'max_expected_profit': max_expected_profit
        }
    return None

# ==========================================
# STEP 3: REINVESTMENT ENGINE
# ==========================================
def process_trade_closure(trade_outcome, capital_pool):
    """
    Manages active trade closure and tracks the fractional dividend sweep loop.
    """
    options_cash = capital_pool['options_cash']
    dividend_vault = capital_pool['dividend_vault']
    
    print(f"\n--- Processing Closed Position for {trade_outcome['ticker']} ---")
    
    if trade_outcome['status'] == 'Profit Target Met':
        net_profit = trade_outcome['max_premium'] * 0.50
        print(f"✅ Success: Hit 50% Profit Target. Net Gain: ${net_profit:.2f}")
        
        if net_profit >= FRACTIONAL_MINIMUM:
            dividend_vault += net_profit
            print(f"💰 Fractional Sweep: ${net_profit:.2f} routed directly to purchase {TARGET_DIVIDEND_ETF}.")
        else:
            options_cash += net_profit
            print(f"⏳ Capital Saved: ${net_profit:.2f} held in cash until collective balance clears the $5 Public fractional floor.")
            
    elif trade_outcome['status'] == 'Assigned':
        print(f"⚠️ Assigned: Stock fell below Put strike. You now own 100 shares.")
        print(f"📦 Pivot Execution: Initiating Covered Call Calculator Module to write options.")
        
    capital_pool['options_cash'] = options_cash
    capital_pool['dividend_vault'] = dividend_vault
    return capital_pool

# ==========================================
# EXECUTION TEST RUN
# ==========================================
if __name__ == "__main__":
    # Portfolio Capital Tracker
    portfolio = {'options_cash': STARTING_CAPITAL, 'dividend_vault': 0.00}
    
    # SCENARIO A: A Cash-Secured Put gets assigned. You acquire 100 shares.
    print("====== SCENARIO: PIVOT TO COVERED CALLS ======")
    assigned_stock_ticker = "XYZ"
    original_put_strike = 2.50  # This is now your Cost Basis per share
    current_market_price = 2.45 # Stock dropped slightly below strike
    implied_volatility = 0.60    # 60% Implied Volatility
    
    # Run the Covered Call Calculator
    cc_setup = maximize_covered_call_expectations(
        cost_basis=original_put_strike,
        current_stock_price=current_market_price,
        iv=implied_volatility
    )
    
    if cc_setup:
        print(f"\n🎯 [AI RECOMMENDED COVERED CALL SELECTION FOR {assigned_stock_ticker}]:")
        print(f"   Action: Sell to Open {assigned_stock_ticker} ${cc_setup['strike']:.2f} Call")
        print(f"   Delta: {cc_setup['delta']} (Optimal odds of retention)")
        print(f"   Immediate Premium Cash Inflow: +${cc_setup['estimated_premium']:.2f}")
        print(f"   Potential Capital Gains Upside: +${cc_setup['capital_gain_potential']:.2f}")
        print(f"   🚀 Maximum Total Profit Yield: ${cc_setup['max_expected_profit']:.2f}")
    else:
        print("\n❌ No optimal Covered Call strike found matching risk/delta parameters.")
        
