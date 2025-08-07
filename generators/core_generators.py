"""
Core generators for fake log entries.
"""

import random
import uuid
from datetime import datetime, timedelta, timezone
from faker import Faker

# Default dates: 3 years ago to now
DEFAULT_START_DATE = datetime.now(timezone.utc) - timedelta(days=3 * 365)
DEFAULT_END_DATE = datetime.now(timezone.utc)

# Log level constants
LOG_LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
LOG_LEVEL_WEIGHTS = [70, 15, 10, 5]

# HTTP method constants
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]
HTTP_METHOD_WEIGHTS = [25, 60, 10, 5]

# HTTP protocol constants
HTTP_PROTOCOLS = ["HTTP/1.1", "HTTP/2", "HTTP/3"]
HTTP_PROTOCOL_WEIGHTS = [60, 35, 5]

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
    10,  # /api/v1/comments
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

# Query parameter types with realistic distribution
QUERY_PARAM_TYPES = ["none", "pagination", "filtering", "sorting", "search"]
QUERY_PARAM_WEIGHTS = [40, 25, 20, 10, 5]

# Common parameter patterns
PAGINATION_PARAMS = [
    "page=1&limit=10",
    "page=2&limit=20",
    "page=1&limit=50",
    "page=3&limit=25",
    "offset=0&limit=10",
    "offset=20&limit=20"
]

FILTERING_PARAMS = [
    "status=active",
    "status=pending",
    "category=posts",
    "category=comments",
    "user_id=123",
    "created_after=2024-01-01",
    "status=active&category=posts",
    "user_id=456&status=active",
    "category=comments&status=pending"
]

SORTING_PARAMS = [
    "sort=created_at&order=desc",
    "sort=updated_at&order=asc",
    "sort=name&order=asc",
    "sort=id&order=desc",
    "sort_by=created_at&sort_order=desc"
]

SEARCH_PARAMS = [
    "q=user+search",
    "q=post+content",
    "q=comment+text",
    "search=api+query",
    "query=test+data"
]

fake = Faker()

# Timestamp generators
def generate_timestamp(start_date: datetime = DEFAULT_START_DATE, end_date: datetime = DEFAULT_END_DATE) -> datetime:
    """Return a single UTC timestamp as datetime object."""
    if end_date < start_date:
        raise ValueError(f"end_date ({end_date}) cannot be before start_date ({start_date})")
    
    timestamp = fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=timezone.utc)
    return timestamp

def generate_timestamps(count: int, start_date: datetime = DEFAULT_START_DATE, end_date: datetime = DEFAULT_END_DATE, sort: bool = True) -> list[datetime]:
    """Return a list of UTC timestamps as datetime objects.
    
    Args:
        count: Number of timestamps to generate
        start_date: Start of date range (default: 3 years ago)
        end_date: End of date range (default: now)
        sort: If True, sort timestamps chronologically (default: True)
    
    Returns:
        List of datetime objects in UTC timezone
    """
    if end_date < start_date:
        raise ValueError(f"end_date ({end_date}) cannot be before start_date ({start_date})")
    
    timestamps = [generate_timestamp(start_date, end_date) for _ in range(count)]
    if sort:
        timestamps.sort()
    return timestamps

# Request ID generators
def generate_request_id() -> uuid.UUID:
    """Return a single request ID as a UUID object."""
    return uuid.uuid4()

def generate_request_ids(count: int) -> list[uuid.UUID]:
    """Return a list of unique request IDs."""
    return [generate_request_id() for _ in range(count)]

# Log level generators
def generate_log_level() -> str:
    """Return a single log level with realistic distribution."""
    return random.choices(LOG_LEVELS, weights=LOG_LEVEL_WEIGHTS)[0]

def generate_log_levels(count: int) -> list[str]:
    """Return a list of log levels with realistic distribution."""
    return [generate_log_level() for _ in range(count)]

# HTTP method generators
def generate_method() -> str:
    """Return a single HTTP method with realistic distribution."""
    return random.choices(HTTP_METHODS, weights=HTTP_METHOD_WEIGHTS)[0]

def generate_methods(count: int) -> list[str]:
    """Return a list of HTTP methods with realistic distribution."""
    return [generate_method() for _ in range(count)]

# HTTP protocol generators
def generate_protocol() -> str:
    """Return a single HTTP protocol with realistic distribution."""
    return random.choices(HTTP_PROTOCOLS, weights=HTTP_PROTOCOL_WEIGHTS)[0]

def generate_protocols(count: int) -> list[str]:
    """Return a list of HTTP protocols with realistic distribution."""
    return [generate_protocol() for _ in range(count)]

# Path generators
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

# Query parameters generators
def generate_query_parameters() -> str:
    """Return a single query parameter string with realistic distribution."""
    param_type = random.choices(QUERY_PARAM_TYPES, weights=QUERY_PARAM_WEIGHTS)[0]
    
    if param_type == "none":
        return ""
    elif param_type == "pagination":
        return "?" + random.choice(PAGINATION_PARAMS)
    elif param_type == "filtering":
        return "?" + random.choice(FILTERING_PARAMS)
    elif param_type == "sorting":
        return "?" + random.choice(SORTING_PARAMS)
    elif param_type == "search":
        return "?" + random.choice(SEARCH_PARAMS)
    
    return ""

def generate_query_parameters_list(count: int) -> list[str]:
    """Return a list of query parameter strings with realistic distribution."""
    return [generate_query_parameters() for _ in range(count)] 