"""
Test PostgreSQL exporter.
"""

import pytest
from datetime import datetime, timezone
import uuid
from exporters.postgres_exporter import (
    get_postgres_create_table_sql,
    get_postgres_insert_sql,
    convert_to_postgres_value,
    generate_insert_values
)

def test_get_postgres_create_table_sql():
    """Test table creation SQL generation."""
    sql = get_postgres_create_table_sql()
    
    # Check that it contains expected table structure
    assert "CREATE TABLE IF NOT EXISTS log_entries" in sql
    assert "timestamp TIMESTAMPTZ NOT NULL" in sql
    assert "request_id UUID NOT NULL" in sql
    assert "log_level VARCHAR(10)" in sql
    assert "status_code INTEGER" in sql
    
    # Check that it contains indexes
    assert "CREATE INDEX IF NOT EXISTS" in sql
    assert "idx_log_entries_timestamp" in sql
    assert "idx_log_entries_log_level" in sql
    assert "idx_log_entries_status_code" in sql

def test_get_postgres_insert_sql():
    """Test INSERT SQL template generation."""
    sql = get_postgres_insert_sql()
    
    # Check that it contains expected INSERT structure
    assert "INSERT INTO log_entries" in sql
    assert "timestamp, request_id, method" in sql
    assert "VALUES" in sql
    assert "%s" in sql  # Should have placeholders
    
    # Count placeholders (should be 23 for all fields)
    placeholder_count = sql.count("%s")
    assert placeholder_count == 23

def test_convert_to_postgres_value_datetime():
    """Test datetime conversion for PostgreSQL."""
    dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
    result = convert_to_postgres_value(dt)
    assert result == dt  # Should return datetime object unchanged

def test_convert_to_postgres_value_uuid():
    """Test UUID conversion for PostgreSQL."""
    test_uuid = uuid.uuid4()
    result = convert_to_postgres_value(test_uuid)
    assert result == test_uuid  # Should return UUID object unchanged

def test_convert_to_postgres_value_string():
    """Test string conversion for PostgreSQL."""
    result = convert_to_postgres_value("test string")
    assert result == "test string"

def test_convert_to_postgres_value_number():
    """Test number conversion for PostgreSQL."""
    result = convert_to_postgres_value(42)
    assert result == 42

def test_convert_to_postgres_value_none():
    """Test None conversion for PostgreSQL."""
    result = convert_to_postgres_value(None)
    assert result is None

def test_convert_to_postgres_value_other():
    """Test other type conversion for PostgreSQL."""
    result = convert_to_postgres_value([1, 2, 3])
    assert result == "[1, 2, 3]"  # Should convert to string

def test_convert_to_postgres_value_string_types():
    """Test string type conversion for PostgreSQL."""
    # Test various string types that our generators return
    test_strings = [
        "192.168.1.1",  # IP address
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",  # User agent
        "https://example.com/page",  # Referer
        "john_doe",  # Username
        "john@example.com",  # Email
        "550e8400-e29b-41d4-a716-446655440000",  # UUID string
        "ff00aa",  # Hex string
        "",  # Empty string
    ]
    
    for test_string in test_strings:
        result = convert_to_postgres_value(test_string)
        assert result == test_string  # Should remain unchanged

def test_generate_insert_values():
    """Test generating insert values from data."""
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
    
    fieldnames = ["timestamp", "request_id", "log_level", "status_code"]
    values = generate_insert_values(data, fieldnames)
    
    assert len(values) == 2  # Two rows
    assert len(values[0]) == 4  # Four fields per row
    
    # Check first row
    assert isinstance(values[0][0], datetime)  # timestamp
    assert isinstance(values[0][1], uuid.UUID)  # request_id
    assert values[0][2] == "INFO"  # log_level
    assert values[0][3] == 200  # status_code
    
    # Check second row
    assert isinstance(values[1][0], datetime)  # timestamp
    assert isinstance(values[1][1], uuid.UUID)  # request_id
    assert values[1][2] == "ERROR"  # log_level
    assert values[1][3] == 500  # status_code

def test_generate_insert_values_missing_fields():
    """Test generating insert values with missing fields."""
    data = [
        {
            "timestamp": datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc),
            "log_level": "INFO"
            # Missing request_id and status_code
        }
    ]
    
    fieldnames = ["timestamp", "request_id", "log_level", "status_code"]
    values = generate_insert_values(data, fieldnames)
    
    assert len(values) == 1
    assert len(values[0]) == 4
    
    # Check that missing fields are None
    assert isinstance(values[0][0], datetime)  # timestamp
    assert values[0][1] is None  # request_id (missing)
    assert values[0][2] == "INFO"  # log_level
    assert values[0][3] is None  # status_code (missing)

def test_generate_insert_values_empty_data():
    """Test generating insert values with empty data."""
    values = generate_insert_values([], ["timestamp", "request_id"])
    assert values == [] 