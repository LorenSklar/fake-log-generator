"""
Test session ID generator.
"""

import pytest
import re
from collections import Counter
from generators.session_id_generator import generate_session_id, generate_session_ids, SESSION_ID_TYPES, SESSION_ID_WEIGHTS

def test_generate_session_id():
    """Test single session ID generation."""
    session_id = generate_session_id()
    
    # Check format
    assert isinstance(session_id, str)

def test_generate_session_ids():
    """Test generating multiple session IDs."""
    count = 10
    session_ids = generate_session_ids(count)
    
    assert len(session_ids) == count
    
    # All should be valid session IDs
    for sid in session_ids:
        assert isinstance(sid, str)

def test_empty_session_ids():
    """Test generating zero session IDs."""
    session_ids = generate_session_ids(0)
    assert session_ids == []

def test_session_id_distribution():
    """Test that session IDs follow realistic distribution."""
    count = 1000
    session_ids = generate_session_ids(count)
    
    # Count different types
    uuid_count = sum(1 for sid in session_ids if sid and re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', sid))
    hex_count = sum(1 for sid in session_ids if sid and re.match(r'^[0-9a-f]{6}$', sid))
    empty_count = sum(1 for sid in session_ids if sid == "")
    
    # Should have some of each type
    assert uuid_count > 0
    assert hex_count > 0
    
    # UUIDs should be most common
    assert uuid_count > hex_count

def test_session_id_formats():
    """Test that session IDs follow proper formats."""
    session_id = generate_session_id()
    
    if session_id:  # If not empty
        # Should be one of: UUID or hex
        is_uuid = bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', session_id))
        is_hex = bool(re.match(r'^[0-9a-f]{6}$', session_id))
        
        assert is_uuid or is_hex 