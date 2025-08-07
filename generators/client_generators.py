"""
Client information generators for fake log entries.
"""

import random
import uuid
from faker import Faker

# IP types with realistic distribution
IP_TYPES = ["ipv4", "ipv6", "private_ip"]
IP_TYPE_WEIGHTS = [70, 20, 10]  # Realistic distribution: mostly IPv4, some IPv6, some private

# Referer types with realistic distribution
REFERER_TYPES = ["url", "none"]
REFERER_WEIGHTS = [60, 40]  # Realistic distribution: some have referers, some don't

# User ID types with realistic distribution
USER_ID_TYPES = ["uuid", "username", "email", "none"]
USER_ID_WEIGHTS = [50, 30, 15, 5]  # Realistic distribution: mostly UUIDs, some usernames, some emails, some none

# Session ID types with realistic distribution
SESSION_ID_TYPES = ["uuid", "hex", "none"]
SESSION_ID_WEIGHTS = [70, 20, 10]  # Realistic distribution: mostly UUIDs, some hex, some none

fake = Faker()

# Source IP generators
def generate_source_ip() -> str:
    """Return a single source IP address with realistic distribution."""
    ip_type = random.choices(IP_TYPES, weights=IP_TYPE_WEIGHTS)[0]
    
    if ip_type == "ipv4":
        return fake.ipv4()
    elif ip_type == "ipv6":
        return fake.ipv6()
    else:  # private_ip
        # Generate private IP ranges manually
        private_ranges = [
            f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
            f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
            f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        ]
        return random.choice(private_ranges)

def generate_source_ips(count: int) -> list[str]:
    """Return a list of source IP addresses with realistic distribution."""
    return [generate_source_ip() for _ in range(count)]

# User agent generators
def generate_user_agent() -> str:
    """Return a single user agent string."""
    return fake.user_agent()

def generate_user_agents(count: int) -> list[str]:
    """Return a list of user agent strings."""
    return [generate_user_agent() for _ in range(count)]

# Referer generators
def generate_referer() -> str:
    """Return a single referer URL with realistic distribution."""
    referer_type = random.choices(REFERER_TYPES, weights=REFERER_WEIGHTS)[0]
    
    if referer_type == "url":
        return fake.url()
    else:  # none
        return ""

def generate_referers(count: int) -> list[str]:
    """Return a list of referer URLs with realistic distribution."""
    return [generate_referer() for _ in range(count)]

# User ID generators
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

# Session ID generators
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