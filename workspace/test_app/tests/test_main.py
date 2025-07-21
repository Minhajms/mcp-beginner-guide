"""
Tests for main module
"""
import pytest
from src.main import main

def test_main():
    """Test that main function runs without error"""
    try:
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised {e}")
