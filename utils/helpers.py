"""
Utility helper functions
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency with proper symbol and formatting"""
    if amount is None:
        return "N/A"
    
    currency_symbols = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€"
    }
    
    symbol = currency_symbols.get(currency, "")
    
    # Indian number formatting
    if currency == "INR":
        # Convert to lakhs format
        if amount >= 100000:
            return f"{symbol}{amount/100000:.2f}L"
        else:
            return f"{symbol}{amount:,.0f}"
    
    return f"{symbol}{amount:,.2f}"

def format_date(date_obj: Any) -> str:
    """Format date object to readable string"""
    if date_obj is None:
        return "N/A"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj)
        except:
            return date_obj
    
    return date_obj.strftime("%B %d, %Y")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def calculate_percentage(part: int, total: int) -> float:
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)

def log_execution_time(func):
    """Decorator to log function execution time"""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"{func.__name__} executed in {duration:.2f} seconds")
        return result
    return wrapper
