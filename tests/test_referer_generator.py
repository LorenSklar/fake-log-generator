"""
Test referer generator.
"""

import pytest
from collections import Counter
from generators.referer_generator import generate_referer, generate_referers, REFERER_TYPES, REFERER_WEIGHTS

def test_generate_referer():
    """Test single referer generation."""
    referer = generate_referer()
    
    # Check format
    assert isinstance(referer, str)
    
    # Should be empty or a valid URL
    if referer:
        assert referer.startswith(("http://", "https://"))

def test_generate_referers():
    """Test generating multiple referers."""
    count = 10
    referers = generate_referers(count)
    
    assert len(referers) == count
    
    # All should be valid referers
    for ref in referers:
        assert isinstance(ref, str)
        if ref:  # If not empty
            assert ref.startswith(("http://", "https://"))

def test_empty_referers():
    """Test generating zero referers."""
    referers = generate_referers(0)
    assert referers == []

def test_referer_distribution():
    """Test that referers follow realistic distribution."""
    count = 1000
    referers = generate_referers(count)
    
    # Count empty vs non-empty
    empty_count = sum(1 for r in referers if r == "")
    non_empty_count = count - empty_count
    
    # Should have some empty (around 40%) and some with URLs (around 60%)
    empty_percentage = empty_count / count
    assert 0.3 < empty_percentage < 0.5  # Allow some variance

def test_referer_format():
    """Test that referers follow proper URL format."""
    referer = generate_referer()
    
    if referer:  # If not empty
        # Should be a valid URL format
        assert referer.startswith(("http://", "https://"))
        assert "." in referer  # Should have a domain 