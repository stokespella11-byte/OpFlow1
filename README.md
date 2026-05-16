# OpFlow - Options Trading Automation

Automated bull put spread options trading strategy for dividend savings using Public.com's API and LangChain.

## Features

- **Account Verification**: Check available uninvested cash balance
- **Options Scanning**: Identify high-yield put spreads 14-21 days out at safe -0.15 delta
- **Automated Execution**: Route multi-leg bull put spreads directly to Public.com

## Prerequisites

- Python 3.8+
- Public.com account with API access
- API credentials (secret key and account ID)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/stokespella11-byte/OpFlow1.git
cd OpFlow1
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your Public.com credentials
```

Add your Public.com API credentials to `.env`:
```
PUBLIC_COM_SECRET=your_secret_key_here
PUBLIC_COM_ACCOUNT_ID=your_account_id_here
```

## Usage

### Run the main script
```bash
python main.py
```

This will:
1. Verify your account capital
2. Scan SPY, QQQ, and IWM options for high-yield spreads
3. Display potential trade opportunities

### Use as a module
```python
from opflow.tools import verify_account_capital, fetch_high_yield_chain

# Check account balance
capital = verify_account_capital()
print(f"Available: ${capital}")

# Scan options chain
result = fetch_high_yield_chain("QQQ")
print(result)
```

## Tools Available

### `verify_account_capital()`
Returns the available uninvested cash balance from your account.

**Returns:** `float` - Available capital

### `fetch_high_yield_chain(ticker: str)`
Scans the options chain for the specified ticker between 14-21 days to expiration.

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., "SPY", "QQQ")

**Returns:** `str` - Formatted spread opportunity details

### `execute_bull_put_spread(ticker: str, short_strike: float, long_strike: float)`
Executes a bull put vertical spread on Public.com.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `short_strike` (float): Strike price to sell
- `long_strike` (float): Strike price to buy (protection)

**Returns:** `str` - Order confirmation or error message

## Strategy Details

**Bull Put Spread:**
- Sells an out-of-the-money (OTM) put
- Buys a protective put 3 strikes lower
- Targets -0.15 delta for defined risk
- 14-21 days to expiration for optimal decay
- Calculates annualized yield based on margin requirement

## Safety Considerations

⚠️ **Important:**
- This is an automated trading system. Test thoroughly before live trading
- Ensure you understand the risks of options trading
- Start with small position sizes
- Monitor your account regularly
- Have stop-loss procedures in place
- **Never commit credentials to version control**

## Configuration

Edit `opflow/tools.py` to adjust:
- Expiration date range (currently 14-21 days)
- Target delta (currently -0.15)
- Strike width (currently 3 points)
- Margin calculation (currently $300)

## Troubleshooting

### ImportError: No module named 'publicdotcom_py'
```bash
pip install --upgrade publicdotcom-py
```

### "Error gathering options market data"
- Verify your API credentials are correct
- Check that the market is open
- Ensure the ticker symbol is valid

### "Could not locate a matching 3-point wide protective put"
- The ticker may not have options available
- Try a different expiration range
- Try a more liquid underlying (SPY, QQQ, etc.)

## License

MIT

## Support

For issues or questions, please open a GitHub issue.

---

**Disclaimer:** This tool is for educational purposes. Options trading involves significant risk. Past performance does not guarantee future results. Trade at your own risk.
