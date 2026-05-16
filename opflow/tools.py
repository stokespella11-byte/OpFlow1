"""OpFlow Trading Tools

LangChain tools for options trading automation with Public.com API.
"""

import os
from langchain.tools import tool
from publicdotcom_py import PublicClient

# Initialize the official Public brokerage client
client = PublicClient(
    secret_key=os.getenv("PUBLIC_COM_SECRET"),
    account_id=os.getenv("PUBLIC_COM_ACCOUNT_ID")
)


@tool
def verify_account_capital() -> float:
    """Queries Public.com to return the exact available uninvested cash balance."""
    balances = client.get_account_balances()
    return float(balances.get("uninvested_cash", 0.0))


@tool
def fetch_high_yield_chain(ticker: str) -> str:
    """
    Scans the options chain for the ticker between 14-21 days out.
    Filters for high-yield puts near a safe -0.15 Delta, 
    matching them with protection 3 strikes lower. Returns the data layout.
    """
    try:
        # Pull market chains via Public API
        chain = client.get_options_chain(ticker=ticker, expiration_days_range=(14, 21))
        puts = chain.get("puts", [])
        
        # Filter for our safe target boundary (-0.15 Delta)
        target_short = min(puts, key=lambda x: abs(x.get("delta", 0) - (-0.15)))
        short_strike = target_short.get("strike")
        
        # Locate the protective long put exactly 3 points lower
        target_long = next((p for p in puts if p.get("strike") == (short_strike - 3)), None)
        
        if not target_long:
            return "Error: Could not locate a matching 3-point wide protective put."
            
        # Calculate annualized yield efficiency metric
        estimated_credit = target_short.get("bid", 0) - target_long.get("ask", 0)
        margin_lock = 300.0 - (estimated_credit * 100)
        annualized_yield = (estimated_credit * 100 / margin_lock) * (365 / 18) * 100

        return (
            f"Asset: {ticker} | Short Strike: ${short_strike} (Delta: {target_short['delta']}) | "
            f"Long Strike: ${target_long['strike']} | Est. Credit: ${estimated_credit:.2f} | "
            f"Capital Required: ${margin_lock:.2f} | Est. Annualized Option Yield: {annualized_yield:.1f}%"
        )
    except Exception as e:
        return f"Error gathering options market data: {str(e)}"


@tool
def execute_bull_put_spread(ticker: str, short_strike: float, long_strike: float) -> str:
    """Routes a multi-leg Bull Put Vertical Spread directly to Public's execution router."""
    try:
        # Native multi-leg layout block utilized by Public's structural API surface
        order_legs = [
            {"side": "sell", "type": "put", "strike": short_strike, "quantity": 1},
            {"side": "buy", "type": "put", "strike": long_strike, "quantity": 1}
        ]
        
        # Pre-flight check and direct submission
        order_receipt = client.place_multileg_order(
            ticker=ticker,
            legs=order_legs,
            duration="gtc",
            price_type="mid"
        )
        return f"Success! Order routed via API. Order ID: {order_receipt.get('order_id')}"
    except Exception as e:
        return f"Execution rejected by Public risk controller: {str(e)}"
