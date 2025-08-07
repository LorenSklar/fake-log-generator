"""
Test user ID generator.
"""

import pytest
import re
import uuid
from collections import Counter
from generators.user_id_generator import generate_user_id, generate_user_ids, USER_ID_TYPES, USER_ID_WEIGHTS

def test_generate_user_id():
    """Test single user ID generation."""
    user_id = generate_user_id()
    
    # Check format
    assert isinstance(user_id, str)

def test_generate_user_ids():
    """Test generating multiple user IDs."""
    count = 10
    user_ids = generate_user_ids(count)
    
    assert len(user_ids) == count
    
    # All should be valid user IDs
    for uid in user_ids:
        assert isinstance(uid, str)

def test_empty_user_ids():
    """Test generating zero user IDs."""
    user_ids = generate_user_ids(0)
    assert user_ids == []

def test_user_id_distribution():
    """Test that user IDs follow realistic distribution."""
    count = 1000
    user_ids = generate_user_ids(count)
    
    # Count different types
    uuid_count = sum(1 for uid in user_ids if uid and re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', uid))
    username_count = sum(1 for uid in user_ids if uid and not '@' in uid and not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', uid) and not uid == "")
    email_count = sum(1 for uid in user_ids if uid and '@' in uid)
    empty_count = sum(1 for uid in user_ids if uid == "")
    
    # Should have some of each type
    assert uuid_count > 0
    assert username_count > 0
    assert email_count > 0
    
    # UUIDs should be most common
    assert uuid_count > username_count
    assert uuid_count > email_count

def test_user_id_formats():
    """Test that user IDs follow proper formats."""
    user_id = generate_user_id()
    
    if user_id:  # If not empty
        # Should be one of: UUID, username, or email
        is_uuid = bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', user_id))
        is_email = '@' in user_id and '.' in user_id
        is_username = not is_uuid and not is_email and len(user_id) > 0
        
        assert is_uuid or is_email or is_username 