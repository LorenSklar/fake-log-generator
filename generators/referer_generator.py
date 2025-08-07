"""
Referer generator for fake log entries.
"""

import random
from faker import Faker

# Referer types with realistic distribution
REFERER_TYPES = ["url", "none"]
REFERER_WEIGHTS = [60, 40]  # Realistic distribution: some have referers, some don't

fake = Faker()

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