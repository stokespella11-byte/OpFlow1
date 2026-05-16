import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup file logging
log_file = 'trading_log.txt'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def log_trade_event(event_type, ticker, details):
    """Log trading events to file."""
    message = f"[{event_type}] {ticker} - {details}"
    logger.info(message)
    print(message)

def log_error(error_message):
    """Log errors to file."""
    logger.error(error_message)
    print(f"❌ ERROR: {error_message}")

def log_success(success_message):
    """Log successful operations."""
    logger.info(success_message)
    print(f"✅ {success_message}")

# Initialize logging on module import
if __name__ == "__main__":
    logger.info("OpFlow1 trading system initialized")
    logger.info("Ready for market operations")
    print(f"Logging active: {log_file}")
