"""
HTTP method generator for fake log entries.
"""

import random

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]
HTTP_METHOD_WEIGHTS = [25, 60, 10, 5]

def generate_method() -> str:
    """Return a single HTTP method with realistic distribution."""
    return random.choices(HTTP_METHODS, weights=HTTP_METHOD_WEIGHTS)[0]

def generate_methods(count: int) -> list[str]:
    """Return a list of HTTP methods with realistic distribution."""
    return [generate_method() for _ in range(count)] 