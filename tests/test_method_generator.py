"""
Test HTTP method generator.
"""

import pytest
from collections import Counter
from generators.method_generator import generate_method, generate_methods, HTTP_METHODS, HTTP_METHOD_WEIGHTS

def test_generate_method():
    """Test single HTTP method generation."""
    method = generate_method()
    
    # Check format
    assert isinstance(method, str)
    assert method in HTTP_METHODS

def test_generate_methods():
    """Test generating multiple HTTP methods."""
    count = 10
    methods = generate_methods(count)
    
    assert len(methods) == count
    
    # All should be valid HTTP methods
    for method in methods:
        assert method in HTTP_METHODS

def test_empty_methods():
    """Test generating zero HTTP methods."""
    methods = generate_methods(0)
    assert methods == []

def test_method_distribution():
    """Test that HTTP methods follow realistic distribution."""
    count = 1000
    methods = generate_methods(count)
    
    # Count occurrences
    counter = Counter(methods)
    
    # Check that all methods are present
    assert set(counter.keys()) == set(HTTP_METHODS)
    
    # Check that POST is most common (should be around 60%)
    post_percentage = counter["POST"] / count
    assert 0.5 < post_percentage < 0.7  # Allow some variance
    
    # Check that GET is second most common (should be around 25%)
    get_percentage = counter["GET"] / count
    assert 0.2 < get_percentage < 0.3  # Allow some variance
    
    # Check that POST is more common than GET
    assert counter["POST"] > counter["GET"]
    
    # Check that GET is more common than PUT
    assert counter["GET"] > counter["PUT"]

def test_method_values():
    """Test that generated values are valid HTTP methods."""
    method = generate_method()
    
    valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
    assert method in valid_methods

def test_no_options_method():
    """Test that OPTIONS method is never generated (weight 0)."""
    count = 1000
    methods = generate_methods(count)
    
    # OPTIONS should never appear since weight is 0
    assert "OPTIONS" not in methods 