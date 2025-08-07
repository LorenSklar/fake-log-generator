"""
Test log entry factory.
"""

import pytest
import json
from datetime import datetime
import uuid
from generators.log_entry_factory import (
    generate_log_entry, generate_log_entries, 
    format_log_entry_as_string, generate_log_lines
)

def test_generate_log_entry():
    """Test single log entry generation."""
    log_entry = generate_log_entry()
    
    # Check that all required fields are present
    required_fields = [
        "timestamp", "log_level", "request_id", "source_ip",
        "method", "path", "query_parameters", "protocol",
        "user_agent", "referer", "user_id", "session_id",
        "status_code", "response_time_ms", "request_headers",
        "request_body", "response_headers", "response_body",
        "service_name", "env", "error_message", "stack_trace"
    ]
    
    for field in required_fields:
        assert field in log_entry
    
    # Check data types
    assert isinstance(log_entry["timestamp"], datetime)
    assert isinstance(log_entry["request_id"], uuid.UUID)
    assert isinstance(log_entry["log_level"], str)
    assert isinstance(log_entry["source_ip"], str)
    assert isinstance(log_entry["method"], str)
    assert isinstance(log_entry["path"], str)
    assert isinstance(log_entry["query_parameters"], str)
    assert isinstance(log_entry["protocol"], str)
    assert isinstance(log_entry["user_agent"], str)
    assert isinstance(log_entry["referer"], str)
    assert isinstance(log_entry["user_id"], str)
    assert isinstance(log_entry["session_id"], str)

def test_generate_log_entries():
    """Test multiple log entries generation."""
    count = 5
    log_entries = generate_log_entries(count)
    
    assert len(log_entries) == count
    
    # All should be valid log entries
    for entry in log_entries:
        assert "timestamp" in entry
        assert "request_id" in entry
        assert "log_level" in entry

def test_empty_log_entries():
    """Test generating zero log entries."""
    log_entries = generate_log_entries(0)
    assert log_entries == []

def test_format_log_entry_json():
    """Test JSON formatting."""
    log_entry = generate_log_entry()
    json_str = format_log_entry_as_string(log_entry, "json")
    
    # Should be valid JSON
    parsed = json.loads(json_str)
    
    # Check that datetime and UUID are converted to strings
    assert isinstance(parsed["timestamp"], str)
    assert isinstance(parsed["request_id"], str)
    
    # Check that other fields are preserved
    assert parsed["log_level"] == log_entry["log_level"]
    assert parsed["source_ip"] == log_entry["source_ip"]
    assert parsed["method"] == log_entry["method"]

def test_format_log_entry_csv():
    """Test CSV formatting."""
    log_entry = generate_log_entry()
    csv_str = format_log_entry_as_string(log_entry, "csv")
    
    # Should be comma-separated
    parts = csv_str.split(",")
    assert len(parts) >= 7  # timestamp,log_level,request_id,source_ip,method,path,status_code
    
    # Check that timestamp is ISO format
    assert "T" in parts[0]  # ISO format has T separator
    
    # Check that request_id is string
    assert parts[2] == str(log_entry["request_id"])

def test_format_log_entry_log():
    """Test traditional log formatting."""
    log_entry = generate_log_entry()
    log_str = format_log_entry_as_string(log_entry, "log")
    
    # Should contain key elements
    assert log_entry["log_level"] in log_str
    assert str(log_entry["request_id"]) in log_str
    assert log_entry["source_ip"] in log_str
    assert log_entry["method"] in log_str
    assert log_entry["path"] in log_str
    assert str(log_entry["status_code"]) in log_str
    
    # Should have traditional log format: timestamp [level] request_id ip method path status
    assert "[" in log_str and "]" in log_str

def test_format_log_entry_invalid():
    """Test invalid format type."""
    log_entry = generate_log_entry()
    
    with pytest.raises(ValueError, match="Unsupported format type"):
        format_log_entry_as_string(log_entry, "invalid")

def test_generate_log_lines():
    """Test generating formatted log lines."""
    count = 3
    log_lines = generate_log_lines(count, "json")
    
    assert len(log_lines) == count
    
    # All should be valid JSON
    for line in log_lines:
        parsed = json.loads(line)
        assert "timestamp" in parsed
        assert "log_level" in parsed

def test_generate_log_lines_csv():
    """Test generating CSV log lines."""
    count = 3
    log_lines = generate_log_lines(count, "csv")
    
    assert len(log_lines) == count
    
    # All should be CSV format
    for line in log_lines:
        parts = line.split(",")
        assert len(parts) >= 7

def test_generate_log_lines_log():
    """Test generating traditional log lines."""
    count = 3
    log_lines = generate_log_lines(count, "log")
    
    assert len(log_lines) == count
    
    # All should be log format
    for line in log_lines:
        assert "[" in line and "]" in line

def test_log_entry_uniqueness():
    """Test that generated log entries have unique request IDs."""
    count = 100
    log_entries = generate_log_entries(count)
    
    request_ids = [entry["request_id"] for entry in log_entries]
    unique_ids = set(request_ids)
    
    # Should have unique request IDs
    assert len(unique_ids) == count

def test_log_entry_realistic_values():
    """Test that log entries contain realistic values."""
    log_entry = generate_log_entry()
    
    # Check log level is valid
    valid_levels = {"INFO", "WARN", "ERROR", "DEBUG"}
    assert log_entry["log_level"] in valid_levels
    
    # Check HTTP method is valid
    valid_methods = {"GET", "POST", "PUT", "DELETE"}
    assert log_entry["method"] in valid_methods
    
    # Check path starts with /api/v1/
    assert log_entry["path"].startswith("/api/v1/")
    
    # Check protocol is valid
    valid_protocols = {"HTTP/1.1", "HTTP/2", "HTTP/3"}
    assert log_entry["protocol"] in valid_protocols
    
    # Check source IP is not empty
    assert log_entry["source_ip"]
    
    # Check user agent is not empty
    assert log_entry["user_agent"] 