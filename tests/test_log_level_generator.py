"""
Test log level generator.
"""

import pytest
from collections import Counter
from generators.log_level_generator import generate_log_level, generate_log_levels, LOG_LEVELS, LOG_LEVEL_WEIGHTS

def test_generate_log_level():
    """Test single log level generation."""
    log_level = generate_log_level()
    
    # Check format
    assert isinstance(log_level, str)
    assert log_level in LOG_LEVELS

def test_generate_log_levels():
    """Test generating multiple log levels."""
    count = 10
    log_levels = generate_log_levels(count)
    
    assert len(log_levels) == count
    
    # All should be valid log levels
    for level in log_levels:
        assert level in LOG_LEVELS

def test_empty_log_levels():
    """Test generating zero log levels."""
    log_levels = generate_log_levels(0)
    assert log_levels == []

def test_log_level_distribution():
    """Test that log levels follow realistic distribution."""
    count = 1000
    log_levels = generate_log_levels(count)
    
    # Count occurrences
    counter = Counter(log_levels)
    
    # Check that all levels are present
    assert set(counter.keys()) == set(LOG_LEVELS)
    
    # Check that INFO is most common (should be around 70%)
    info_percentage = counter["INFO"] / count
    assert 0.6 < info_percentage < 0.8  # Allow some variance
    
    # Check that ERROR is less common than WARN
    assert counter["ERROR"] < counter["WARN"]
    
    # Check that DEBUG is least common
    assert counter["DEBUG"] < counter["ERROR"]

def test_log_level_values():
    """Test that generated values are valid log levels."""
    log_level = generate_log_level()
    
    valid_levels = {"INFO", "WARN", "ERROR", "DEBUG"}
    assert log_level in valid_levels 