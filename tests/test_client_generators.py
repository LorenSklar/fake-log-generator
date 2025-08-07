"""
Test client generators for fake log entries.
"""

import pytest
import re
from collections import Counter
from generators.client_generators import (
    # Source IP generators
    generate_source_ip, generate_source_ips, IP_TYPES, IP_TYPE_WEIGHTS,
    # User agent generators
    generate_user_agent, generate_user_agents,
    # Referer generators
    generate_referer, generate_referers, REFERER_TYPES, REFERER_WEIGHTS,
    # User ID generators
    generate_user_id, generate_user_ids, USER_ID_TYPES, USER_ID_WEIGHTS,
    # Session ID generators
    generate_session_id, generate_session_ids, SESSION_ID_TYPES, SESSION_ID_WEIGHTS
)

# Source IP tests
def test_generate_source_ip():
    """Test single source IP generation."""
    ip = generate_source_ip()
    
    # Check format
    assert isinstance(ip, str)
    assert len(ip) > 0

def test_generate_source_ips():
    """Test generating multiple source IPs."""
    count = 10
    ips = generate_source_ips(count)
    
    assert len(ips) == count
    
    # All should be valid IPs
    for ip in ips:
        assert isinstance(ip, str)
        assert len(ip) > 0

def test_empty_source_ips():
    """Test generating zero source IPs."""
    ips = generate_source_ips(0)
    assert ips == []

def test_ip_distribution():
    """Test that IP types follow realistic distribution."""
    count = 1000
    ips = generate_source_ips(count)
    
    # Count IPv4, IPv6, and private IPs
    ipv4_count = sum(1 for ip in ips if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip))
    ipv6_count = sum(1 for ip in ips if ':' in ip and len(ip) > 15)
    private_count = sum(1 for ip in ips if ip.startswith(('10.', '172.', '192.168.')))
    
    # Should have some of each type
    assert ipv4_count > 0
    assert ipv6_count > 0
    assert private_count > 0
    
    # IPv4 should be most common
    assert ipv4_count > ipv6_count
    assert ipv4_count > private_count

def test_ip_format():
    """Test that IPs follow proper format."""
    ip = generate_source_ip()
    
    # Should be valid IP format
    is_ipv4 = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip))
    is_ipv6 = bool(re.match(r'^[0-9a-fA-F:]+$', ip)) and ':' in ip and len(ip) > 15
    is_private = ip.startswith(('10.', '172.', '192.168.'))
    
    assert is_ipv4 or is_ipv6 or is_private

# User agent tests
def test_generate_user_agent():
    """Test single user agent generation."""
    user_agent = generate_user_agent()
    
    # Check format
    assert isinstance(user_agent, str)
    assert len(user_agent) > 0
    
    # Should contain common user agent patterns
    assert any(pattern in user_agent for pattern in ["Mozilla", "Chrome", "Safari", "Firefox", "Edge", "AppleWebKit"])

def test_generate_user_agents():
    """Test generating multiple user agents."""
    count = 10
    user_agents = generate_user_agents(count)
    
    assert len(user_agents) == count
    
    # All should be valid user agents
    for ua in user_agents:
        assert isinstance(ua, str)
        assert len(ua) > 0

def test_empty_user_agents():
    """Test generating zero user agents."""
    user_agents = generate_user_agents(0)
    assert user_agents == []

def test_user_agent_variety():
    """Test that user agents have variety."""
    count = 100
    user_agents = generate_user_agents(count)
    
    # Should have some variety (not all identical)
    unique_agents = set(user_agents)
    assert len(unique_agents) > 1  # Should have multiple different user agents

# Referer tests
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

# User ID tests
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

# Session ID tests
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