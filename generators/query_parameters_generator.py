"""
Query parameters generator for fake log entries.
"""

import random
from faker import Faker

# Query parameter types with realistic distribution
QUERY_PARAM_TYPES = ["none", "pagination", "filtering", "sorting", "search"]
QUERY_PARAM_WEIGHTS = [40, 25, 20, 10, 5]  # Realistic distribution

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