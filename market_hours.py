#!/usr/bin/env python3
"""
Market Hours Status Checker
Determines if US equity markets are currently open or closed.
"""

from datetime import datetime, time

def is_market_open():
    """
    Check if US stock market is currently open.
    Market hours: 9:30 AM - 4:00 PM ET, Monday-Friday
    """
    now = datetime.now()
    market_open_time = time(9, 30)
    market_close_time = time(16, 0)
    current_time = now.time()
    
    # Check if weekday (Monday=0, Friday=4)
    is_weekday = now.weekday() < 5
    
    # Check if within market hours
    within_hours = market_open_time <= current_time <= market_close_time
    
    return is_weekday and within_hours

def market_status():
    """Return detailed market status."""
    now = datetime.now()
    
    print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    if is_market_open():
        print("📈 Market is OPEN")
        return True
    else:
        print("⏰ Market is CLOSED")
        
        # Determine next market open
        if now.weekday() < 4:  # Monday-Thursday
            next_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
            if now.time() > time(16, 0):
                next_open = next_open.replace(day=now.day + 1)
        elif now.weekday() == 4:  # Friday
            next_open = now.replace(hour=9, minute=30, second=0, microsecond=0, day=now.day + 3)
        else:  # Saturday or Sunday
            days_until_monday = 7 - now.weekday()
            next_open = now.replace(hour=9, minute=30, second=0, microsecond=0, day=now.day + days_until_monday)
        
        print(f"Next Market Open: {next_open.strftime('%Y-%m-%d %H:%M:%S')}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("OpFlow1 - Market Hours Status")
    print("="*50 + "\n")
    
    market_status()
    
    print("\n" + "="*50)
    print("Market Hours: 9:30 AM - 4:00 PM ET (Mon-Fri)")
    print("="*50 + "\n")
