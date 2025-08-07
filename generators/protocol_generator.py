"""
HTTP protocol generator for fake log entries.
"""

import random

# HTTP protocols with realistic distribution for modern APIs
HTTP_PROTOCOLS = ["HTTP/1.1", "HTTP/2", "HTTP/3"]
HTTP_PROTOCOL_WEIGHTS = [60, 35, 5]  # Realistic distribution

def generate_protocol() -> str:
    """Return a single HTTP protocol with realistic distribution."""
    return random.choices(HTTP_PROTOCOLS, weights=HTTP_PROTOCOL_WEIGHTS)[0]

def generate_protocols(count: int) -> list[str]:
    """Return a list of HTTP protocols with realistic distribution."""
    return [generate_protocol() for _ in range(count)] 