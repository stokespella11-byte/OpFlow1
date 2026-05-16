# OpFlow1

Option execute to dividend savings - An automated options trading system for bull put spreads.

## Overview

OpFlow1 is a Python-based options trading automation tool that uses LangChain and the Public.com API to identify and execute high-yield bull put spread strategies.

## Features

- **Account Capital Verification**: Check available uninvested cash balance
- **Options Chain Analysis**: Scan and filter options chains for optimal spreads
- **Automated Execution**: Execute bull put vertical spreads directly via API
- **Yield Calculation**: Compute annualized returns on identified positions

## Setup

### Prerequisites

- Python 3.8+
- Public.com account with API access
- Valid API credentials (secret key and account ID)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/stokespella11-byte/OpFlow1.git
cd OpFlow1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Public.com API credentials
```

## Usage

### Import and Use the Tools

```python
from options_tools import verify_account_capital, fetch_high_yield_chain, execute_bull_put_spread

# Check available capital
capital = verify_account_capital()
print(f"Available Capital: ${capital}")

# Scan for high-yield spreads
chain_data = fetch_high_yield_chain("AAPL")
print(chain_data)

# Execute a spread
result = execute_bull_put_spread("AAPL", short_strike=180.0, long_strike=177.0)
print(result)
```

## Tools Reference

### `verify_account_capital() -> float`
Queries Public.com API to return the available uninvested cash balance.

**Returns**: Float value of uninvested capital

---

### `fetch_high_yield_chain(ticker: str) -> str`
Scans the options chain for high-yield put spreads within 14-21 days.

**Parameters**:
- `ticker` (str): Stock ticker symbol (e.g., "AAPL")

**Returns**: Formatted string with position details including:
- Short strike price and delta
- Long strike price
- Estimated credit
- Required capital
- Estimated annualized yield

---

### `execute_bull_put_spread(ticker: str, short_strike: float, long_strike: float) -> str`
Executes a multi-leg bull put vertical spread order.

**Parameters**:
- `ticker` (str): Stock ticker symbol
- `short_strike` (float): Strike price for the short put
- `long_strike` (float): Strike price for the long put

**Returns**: Order confirmation with order ID or error message

## Configuration

### Key Parameters

- **Delta Target**: -0.15 (safe boundary for short puts)
- **Spread Width**: 3 strike points
- **DTE Range**: 14-21 days to expiration
- **Margin Lock**: Base $300 (adjusted for credit received)
- **Order Duration**: GTC (Good-Till-Canceled)
- **Order Price**: Mid-price

## Important Notes

⚠️ **Risk Warning**: Options trading involves significant risk. This tool is designed for experienced traders.

- Always verify API credentials are correct before execution
- Test with paper trading first
- Monitor position sizing and account equity
- Ensure margin requirements are met before execution
- Public.com API credentials should be kept secure in `.env` file

## Environment Variables

Required environment variables in `.env`:

```
PUBLIC_COM_SECRET=your_secret_key
PUBLIC_COM_ACCOUNT_ID=your_account_id
```

Never commit `.env` to version control.

## License

This project is provided as-is. Use at your own risk.

## Support

For issues with the Public.com API, refer to their official documentation.
