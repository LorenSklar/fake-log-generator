"""
Test request ID generator.
"""

import pytest
import uuid
from generators.request_id_generator import generate_request_id, generate_request_ids

def test_generate_request_id():
    """Test single request ID generation."""
    request_id = generate_request_id()
    
    # Check format
    assert isinstance(request_id, uuid.UUID)
    
    # Check that it's a valid UUID
    assert str(request_id) == str(uuid.UUID(str(request_id)))

def test_generate_request_ids():
    """Test generating multiple request IDs."""
    count = 10
    request_ids = generate_request_ids(count)
    
    assert len(request_ids) == count
    
    # All should be valid UUIDs
    for rid in request_ids:
        assert isinstance(rid, uuid.UUID)

def test_request_ids_unique():
    """Test that generated request IDs are unique."""
    count = 100
    request_ids = generate_request_ids(count)
    
    # Check uniqueness
    unique_ids = set(request_ids)
    assert len(unique_ids) == count

def test_empty_request_ids():
    """Test generating zero request IDs."""
    request_ids = generate_request_ids(0)
    assert request_ids == []

def test_request_id_format():
    """Test that request IDs follow UUID format when converted to string."""
    request_id = generate_request_id()
    request_id_str = str(request_id)
    
    # Should match UUID pattern: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    import re
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    assert re.match(pattern, request_id_str) 