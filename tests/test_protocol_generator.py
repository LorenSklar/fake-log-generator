"""
Test HTTP protocol generator.
"""

import pytest
from collections import Counter
from generators.protocol_generator import generate_protocol, generate_protocols, HTTP_PROTOCOLS, HTTP_PROTOCOL_WEIGHTS

def test_generate_protocol():
    """Test single HTTP protocol generation."""
    protocol = generate_protocol()
    
    # Check format
    assert isinstance(protocol, str)
    assert protocol in HTTP_PROTOCOLS

def test_generate_protocols():
    """Test generating multiple HTTP protocols."""
    count = 10
    protocols = generate_protocols(count)
    
    assert len(protocols) == count
    
    # All should be valid HTTP protocols
    for protocol in protocols:
        assert protocol in HTTP_PROTOCOLS

def test_empty_protocols():
    """Test generating zero HTTP protocols."""
    protocols = generate_protocols(0)
    assert protocols == []

def test_protocol_distribution():
    """Test that HTTP protocols follow realistic distribution."""
    count = 1000
    protocols = generate_protocols(count)
    
    # Count occurrences
    counter = Counter(protocols)
    
    # Check that all protocols are present
    assert set(counter.keys()) == set(HTTP_PROTOCOLS)
    
    # Check that HTTP/1.1 is most common (should be around 60%)
    http11_percentage = counter["HTTP/1.1"] / count
    assert 0.5 < http11_percentage < 0.7  # Allow some variance
    
    # Check that HTTP/2 is second most common (should be around 35%)
    http2_percentage = counter["HTTP/2"] / count
    assert 0.25 < http2_percentage < 0.45  # Allow some variance
    
    # Check that HTTP/1.1 is more common than HTTP/2
    assert counter["HTTP/1.1"] > counter["HTTP/2"]
    
    # Check that HTTP/2 is more common than HTTP/3
    assert counter["HTTP/2"] > counter["HTTP/3"]

def test_protocol_values():
    """Test that generated values are valid HTTP protocols."""
    protocol = generate_protocol()
    
    valid_protocols = {"HTTP/1.1", "HTTP/2", "HTTP/3"}
    assert protocol in valid_protocols

def test_protocol_format():
    """Test that protocols follow proper HTTP format."""
    protocol = generate_protocol()
    
    # Should start with HTTP/
    assert protocol.startswith("HTTP/")
    
    # Should have version number
    version = protocol.split("/")[1]
    assert version in ["1.1", "2", "3"] 