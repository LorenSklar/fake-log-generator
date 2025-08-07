"""
User agent generator for fake log entries.
"""

from faker import Faker

fake = Faker()

def generate_user_agent() -> str:
    """Return a single user agent string."""
    return fake.user_agent()

def generate_user_agents(count: int) -> list[str]:
    """Return a list of user agent strings."""
    return [generate_user_agent() for _ in range(count)] 