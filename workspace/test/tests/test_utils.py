"""
Tests for utility functions
"""
import pytest
from src.utils import safe_divide, format_message

def test_safe_divide():
    """Test safe division function"""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 3) == pytest.approx(2.333, rel=1e-2)
    
    with pytest.raises(ValueError):
        safe_divide(10, 0)

def test_format_message():
    """Test message formatting"""
    assert format_message("test") == "[INFO] test"
    assert format_message("error", "ERROR") == "[ERROR] error"
