"""
Utility functions for the project
"""

def safe_divide(a: float, b: float) -> float:
    """Safely divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def format_message(message: str, prefix: str = "INFO") -> str:
    """Format a message with a prefix"""
    return f"[{prefix}] {message}"
