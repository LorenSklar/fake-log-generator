"""
API path generator for fake log entries.
"""

import random
from faker import Faker

# ID types for path generation
ID_TYPES = ["number", "uuid", "slug"]

# Common API path patterns with realistic distribution
API_PATHS = [
    "/api/v1/users",
    "/api/v1/users/{id}",
    "/api/v1/posts",
    "/api/v1/posts/{id}",
    "/api/v1/comments",
    "/api/v1/comments/{id}",
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/register",
    "/api/v1/profile",
    "/api/v1/settings",
    "/api/v1/notifications",
    "/api/v1/search",
    "/api/v1/upload",
    "/api/v1/download",
    "/api/v1/health",
    "/api/v1/metrics",
    "/api/v1/admin/users",
    "/api/v1/admin/settings"
]

API_PATH_WEIGHTS = [
    25,  # /api/v1/users (most common)
    20,  # /api/v1/users/{id}
    15,  # /api/v1/posts
    10,  # /api/v1/posts/{id}
    10,   # /api/v1/comments
    5,   # /api/v1/comments/{id}
    5,   # /api/v1/auth/login
    3,   # /api/v1/auth/logout
    2,   # /api/v1/auth/register
    1,   # /api/v1/profile
    1,   # /api/v1/settings
    1,   # /api/v1/notifications
    1,   # /api/v1/search
    1,   # /api/v1/upload
    1,   # /api/v1/download
    1,   # /api/v1/health
    1,   # /api/v1/metrics
    1,   # /api/v1/admin/users
    1    # /api/v1/admin/settings
]

fake = Faker()

def generate_path() -> str:
    """Return a single API path with realistic distribution."""
    path_template = random.choices(API_PATHS, weights=API_PATH_WEIGHTS)[0]
    
    # Replace {id} placeholders with realistic IDs
    if "{id}" in path_template:
        # Use realistic ID patterns: numbers, UUIDs, or slugs
        id_type = random.choice(ID_TYPES)
        if id_type == "number":
            id_value = str(random.randint(1, 999999))
        elif id_type == "uuid":
            id_value = str(fake.uuid4())
        else:  # slug
            id_value = fake.slug()
        
        return path_template.replace("{id}", id_value)
    
    return path_template

def generate_paths(count: int) -> list[str]:
    """Return a list of API paths with realistic distribution."""
    return [generate_path() for _ in range(count)] 