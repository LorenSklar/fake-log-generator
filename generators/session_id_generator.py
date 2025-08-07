"""
Session ID generator for fake log entries.
"""

import random
import uuid
from faker import Faker

# Session ID types with realistic distribution
SESSION_ID_TYPES = ["uuid", "hex", "none"]
SESSION_ID_WEIGHTS = [70, 20, 10]  # Realistic distribution: mostly UUIDs, some hex, some none

fake = Faker()

def generate_session_id() -> str:
    """Return a single session ID with realistic distribution."""
    session_id_type = random.choices(SESSION_ID_TYPES, weights=SESSION_ID_WEIGHTS)[0]
    
    if session_id_type == "uuid":
        return str(uuid.uuid4())
    elif session_id_type == "hex":
        return fake.hex_color().replace("#", "")  # 6-character hex
    else:  # none
        return ""

def generate_session_ids(count: int) -> list[str]:
    """Return a list of session IDs with realistic distribution."""
    return [generate_session_id() for _ in range(count)] 