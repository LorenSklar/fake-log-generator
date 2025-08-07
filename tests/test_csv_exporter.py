"""
Test CSV exporter.
"""

import pytest
import tempfile
import os
from datetime import datetime, timezone
import uuid
from exporters.csv_exporter import convert_to_csv_value, export_to_csv

def test_convert_to_csv_value_datetime():
    """Test datetime conversion to CSV string."""
    dt = datetime(2024, 1, 15, 10, 30, 45, 123000, tzinfo=timezone.utc)
    result = convert_to_csv_value(dt)
    assert result == "2024-01-15T10:30:45.123Z"

def test_convert_to_csv_value_uuid():
    """Test UUID conversion to CSV string."""
    test_uuid = uuid.uuid4()
    result = convert_to_csv_value(test_uuid)
    assert result == str(test_uuid)

def test_convert_to_csv_value_string():
    """Test string conversion to CSV string."""
    result = convert_to_csv_value("test string")
    assert result == "test string"

def test_convert_to_csv_value_number():
    """Test number conversion to CSV string."""
    result = convert_to_csv_value(42)
    assert result == "42"

def test_convert_to_csv_value_none():
    """Test None conversion to CSV string."""
    result = convert_to_csv_value(None)
    assert result == ""

def test_export_to_csv():
    """Test CSV file export."""
    data = [
        {
            "timestamp": datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc),
            "request_id": uuid.uuid4(),
            "log_level": "INFO",
            "status_code": 200
        },
        {
            "timestamp": datetime(2024, 1, 15, 10, 31, 0, tzinfo=timezone.utc),
            "request_id": uuid.uuid4(),
            "log_level": "ERROR",
            "status_code": 500
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        filename = tmp.name
    
    try:
        export_to_csv(data, filename)
        
        # Check file exists and has content
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
        
        # Read and verify content
        with open(filename, 'r') as f:
            content = f.read()
            assert "timestamp" in content
            assert "request_id" in content
            assert "INFO" in content
            assert "ERROR" in content
            assert "200" in content
            assert "500" in content
    finally:
        os.unlink(filename)

def test_export_to_csv_empty_data():
    """Test CSV export with empty data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        filename = tmp.name
    
    try:
        export_to_csv([], filename)
        # Should not create file or create empty file
        assert not os.path.exists(filename) or os.path.getsize(filename) == 0
    finally:
        if os.path.exists(filename):
            os.unlink(filename)

def test_export_to_csv_custom_fieldnames():
    """Test CSV export with custom fieldnames."""
    data = [
        {"a": 1, "b": 2, "c": 3},
        {"a": 4, "b": 5, "c": 6}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        filename = tmp.name
    
    try:
        export_to_csv(data, filename, fieldnames=["a", "c"])  # Skip 'b'
        
        with open(filename, 'r') as f:
            content = f.read()
            assert "a,c" in content  # Header should only have a,c
            assert "1,3" in content  # First row
            assert "4,6" in content  # Second row
            assert "2" not in content  # 'b' should not be in output
            assert "5" not in content
    finally:
        os.unlink(filename) 