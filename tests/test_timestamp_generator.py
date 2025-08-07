"""
Test timestamp generator.
"""

import pytest
from datetime import datetime, timedelta, timezone
from generators.timestamp_generator import generate_timestamp, generate_timestamps, DEFAULT_START_DATE, DEFAULT_END_DATE

def test_generate_timestamp():
    """Test single timestamp generation."""
    timestamp = generate_timestamp()
    
    # Check format
    assert isinstance(timestamp, datetime)
    assert timestamp.tzinfo == timezone.utc
    
    # Check that it's within the expected range
    assert DEFAULT_START_DATE <= timestamp <= DEFAULT_END_DATE

def test_generate_timestamp_custom_range():
    """Test timestamp with custom date range."""
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
    
    timestamp = generate_timestamp(start_date, end_date)
    
    assert start_date <= timestamp <= end_date
    assert timestamp.tzinfo == timezone.utc

def test_generate_timestamps():
    """Test generating multiple timestamps."""
    count = 10
    timestamps = generate_timestamps(count)
    
    assert len(timestamps) == count
    
    # All should be valid datetime objects
    for ts in timestamps:
        assert isinstance(ts, datetime)
        assert ts.tzinfo == timezone.utc
        assert DEFAULT_START_DATE <= ts <= DEFAULT_END_DATE
    
    # Should be sorted chronologically (default)
    assert timestamps == sorted(timestamps)

def test_generate_timestamps_sorted():
    """Test generating multiple timestamps with sorting enabled."""
    count = 5
    timestamps = generate_timestamps(count, sort=True)
    
    assert len(timestamps) == count
    assert timestamps == sorted(timestamps)

def test_generate_timestamps_unsorted():
    """Test generating multiple timestamps with sorting disabled."""
    count = 5
    timestamps = generate_timestamps(count, sort=False)
    
    assert len(timestamps) == count
    
    # Should not necessarily be sorted

def test_generate_timestamps_custom_range():
    """Test generating multiple timestamps with custom range."""
    count = 5
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
    
    timestamps = generate_timestamps(count, start_date, end_date)
    
    assert len(timestamps) == count
    
    for ts in timestamps:
        assert start_date <= ts <= end_date
        assert ts.tzinfo == timezone.utc
    
    # Should be sorted chronologically (default)
    assert timestamps == sorted(timestamps)

def test_empty_timestamps():
    """Test generating zero timestamps."""
    timestamps = generate_timestamps(0)
    assert timestamps == [] 