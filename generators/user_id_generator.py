"""
User ID generator for fake log entries.
"""

import random
import uuid
from faker import Faker

# User ID types with realistic distribution
USER_ID_TYPES = ["uuid", "username", "email", "none"]
USER_ID_WEIGHTS = [50, 30, 15, 5]  # Realistic distribution: mostly UUIDs, some usernames, some emails, some none

fake = Faker()

def generate_user_id() -> str:
    """Return a single user ID with realistic distribution."""
    user_id_type = random.choices(USER_ID_TYPES, weights=USER_ID_WEIGHTS)[0]
    
    if user_id_type == "uuid":
        return str(uuid.uuid4())
    elif user_id_type == "username":
        return fake.user_name()
    elif user_id_type == "email":
        return fake.email()
    else:  # none
        return ""

def generate_user_ids(count: int) -> list[str]:
    """Return a list of user IDs with realistic distribution."""
    return [generate_user_id() for _ in range(count)] 