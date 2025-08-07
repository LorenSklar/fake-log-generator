"""
Test source IP generator.
"""

import pytest
import re
from collections import Counter
from generators.source_ip_generator import generate_source_ip, generate_source_ips, IP_TYPES, IP_TYPE_WEIGHTS

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