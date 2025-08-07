"""
Test user agent generator.
"""

import pytest
from generators.user_agent_generator import generate_user_agent, generate_user_agents

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