"""
Source IP generator for fake log entries.
"""

import random
from faker import Faker

# IP types with realistic distribution
IP_TYPES = ["ipv4", "ipv6", "private_ip"]
IP_TYPE_WEIGHTS = [70, 20, 10]  # Realistic distribution: mostly IPv4, some IPv6, some private

fake = Faker()

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