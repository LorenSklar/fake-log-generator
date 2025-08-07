"""
Request ID generator for fake log entries.
"""

import uuid

def generate_request_id() -> uuid.UUID:
    """Return a single request ID as a UUID object."""
    return uuid.uuid4()

def generate_request_ids(count: int) -> list[uuid.UUID]:
    """Return a list of unique request IDs."""
    return [generate_request_id() for _ in range(count)] 