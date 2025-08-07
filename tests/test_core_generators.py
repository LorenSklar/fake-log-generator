"""
Test core generators for fake log entries.
"""

import pytest
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
import uuid
from generators.core_generators import (
    # Timestamp generators
    generate_timestamp, generate_timestamps, DEFAULT_START_DATE, DEFAULT_END_DATE,
    # Request ID generators
    generate_request_id, generate_request_ids,
    # Log level generators
    generate_log_level, generate_log_levels, LOG_LEVELS, LOG_LEVEL_WEIGHTS,
    # HTTP method generators
    generate_method, generate_methods, HTTP_METHODS, HTTP_METHOD_WEIGHTS,
    # HTTP protocol generators
    generate_protocol, generate_protocols, HTTP_PROTOCOLS, HTTP_PROTOCOL_WEIGHTS,
    # Path generators
    generate_path, generate_paths, API_PATHS, API_PATH_WEIGHTS,
    # Query parameters generators
    generate_query_parameters, generate_query_parameters_list, QUERY_PARAM_TYPES, QUERY_PARAM_WEIGHTS
)

# Timestamp tests
def test_generate_timestamp():
    """Test single timestamp generation."""
    timestamp = generate_timestamp()
    
    # Check format
    assert isinstance(timestamp, datetime)
    assert timestamp.tzinfo == timezone.utc
    
    # Check that it's within the expected range
    assert DEFAULT_START_DATE <= timestamp <= DEFAULT_END_DATE

def test_generate_timestamp_custom_range():
    """Test timestamp with custom date range."""
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
    
    timestamp = generate_timestamp(start_date, end_date)
    
    assert start_date <= timestamp <= end_date
    assert timestamp.tzinfo == timezone.utc

def test_generate_timestamps():
    """Test generating multiple timestamps."""
    count = 10
    timestamps = generate_timestamps(count)
    
    assert len(timestamps) == count
    
    # All should be valid datetime objects
    for ts in timestamps:
        assert isinstance(ts, datetime)
        assert ts.tzinfo == timezone.utc
        assert DEFAULT_START_DATE <= ts <= DEFAULT_END_DATE
    
    # Should be sorted chronologically (default)
    assert timestamps == sorted(timestamps)

def test_generate_timestamps_sorted():
    """Test generating multiple timestamps with sorting enabled."""
    count = 5
    timestamps = generate_timestamps(count, sort=True)
    
    assert len(timestamps) == count
    assert timestamps == sorted(timestamps)

def test_generate_timestamps_unsorted():
    """Test generating multiple timestamps with sorting disabled."""
    count = 5
    timestamps = generate_timestamps(count, sort=False)
    
    assert len(timestamps) == count

def test_generate_timestamps_custom_range():
    """Test generating multiple timestamps with custom range."""
    count = 5
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
    
    timestamps = generate_timestamps(count, start_date, end_date)
    
    assert len(timestamps) == count
    
    for ts in timestamps:
        assert start_date <= ts <= end_date
        assert ts.tzinfo == timezone.utc
    
    # Should be sorted chronologically (default)
    assert timestamps == sorted(timestamps)

def test_empty_timestamps():
    """Test generating zero timestamps."""
    timestamps = generate_timestamps(0)
    assert timestamps == []

def test_invalid_date_range():
    """Test that invalid date ranges raise ValueError."""
    start_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 1, tzinfo=timezone.utc)  # Before start_date
    
    with pytest.raises(ValueError, match="end_date.*cannot be before start_date"):
        generate_timestamp(start_date, end_date)
    
    with pytest.raises(ValueError, match="end_date.*cannot be before start_date"):
        generate_timestamps(5, start_date, end_date)

# Request ID tests
def test_generate_request_id():
    """Test single request ID generation."""
    request_id = generate_request_id()
    
    # Check format
    assert isinstance(request_id, uuid.UUID)
    
    # Check that it's a valid UUID
    assert str(request_id) == str(uuid.UUID(str(request_id)))

def test_generate_request_ids():
    """Test generating multiple request IDs."""
    count = 10
    request_ids = generate_request_ids(count)
    
    assert len(request_ids) == count
    
    # All should be valid UUID objects
    for rid in request_ids:
        assert isinstance(rid, uuid.UUID)

def test_request_ids_unique():
    """Test that generated request IDs are unique."""
    count = 100
    request_ids = generate_request_ids(count)
    
    # Check uniqueness
    unique_ids = set(request_ids)
    assert len(unique_ids) == count

def test_empty_request_ids():
    """Test generating zero request IDs."""
    request_ids = generate_request_ids(0)
    assert request_ids == []

def test_request_id_format():
    """Test that request IDs follow UUID format when converted to string."""
    request_id = generate_request_id()
    request_id_str = str(request_id)
    
    # Should match UUID pattern: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    assert re.match(pattern, request_id_str)

# Log level tests
def test_generate_log_level():
    """Test single log level generation."""
    log_level = generate_log_level()
    
    # Check format
    assert isinstance(log_level, str)
    assert log_level in LOG_LEVELS

def test_generate_log_levels():
    """Test generating multiple log levels."""
    count = 10
    log_levels = generate_log_levels(count)
    
    assert len(log_levels) == count
    
    # All should be valid log levels
    for level in log_levels:
        assert level in LOG_LEVELS

def test_empty_log_levels():
    """Test generating zero log levels."""
    log_levels = generate_log_levels(0)
    assert log_levels == []

def test_log_level_distribution():
    """Test that log levels follow realistic distribution."""
    count = 1000
    log_levels = generate_log_levels(count)
    
    # Count occurrences
    counter = Counter(log_levels)
    
    # Check that all levels are present
    assert set(counter.keys()) == set(LOG_LEVELS)
    
    # Check that INFO is most common (should be around 70%)
    info_percentage = counter["INFO"] / count
    assert 0.6 < info_percentage < 0.8  # Allow some variance
    
    # Check that ERROR is less common than WARN
    assert counter["ERROR"] < counter["WARN"]
    
    # Check that DEBUG is least common
    assert counter["DEBUG"] < counter["ERROR"]

def test_log_level_values():
    """Test that generated values are valid log levels."""
    log_level = generate_log_level()
    
    valid_levels = {"INFO", "WARN", "ERROR", "DEBUG"}
    assert log_level in valid_levels

# HTTP method tests
def test_generate_method():
    """Test single HTTP method generation."""
    method = generate_method()
    
    # Check format
    assert isinstance(method, str)
    assert method in HTTP_METHODS

def test_generate_methods():
    """Test generating multiple HTTP methods."""
    count = 10
    methods = generate_methods(count)
    
    assert len(methods) == count
    
    # All should be valid HTTP methods
    for method in methods:
        assert method in HTTP_METHODS

def test_empty_methods():
    """Test generating zero HTTP methods."""
    methods = generate_methods(0)
    assert methods == []

def test_method_distribution():
    """Test that HTTP methods follow realistic distribution."""
    count = 1000
    methods = generate_methods(count)
    
    # Count occurrences
    counter = Counter(methods)
    
    # Check that all methods are present
    assert set(counter.keys()) == set(HTTP_METHODS)
    
    # Check that POST is most common (around 60%)
    post_percentage = counter["POST"] / count
    assert 0.5 < post_percentage < 0.7  # Allow some variance
    
    # Check that GET is second most common (around 25%)
    get_percentage = counter["GET"] / count
    assert 0.2 < get_percentage < 0.3  # Allow some variance
    
    # Check that POST is more common than GET
    assert counter["POST"] > counter["GET"]
    
    # Check that GET is more common than PUT
    assert counter["GET"] > counter["PUT"]

def test_method_values():
    """Test that generated values are valid HTTP methods."""
    method = generate_method()
    
    valid_methods = {"GET", "POST", "PUT", "DELETE"}
    assert method in valid_methods

# HTTP protocol tests
def test_generate_protocol():
    """Test single HTTP protocol generation."""
    protocol = generate_protocol()
    
    # Check format
    assert isinstance(protocol, str)
    assert protocol in HTTP_PROTOCOLS

def test_generate_protocols():
    """Test generating multiple HTTP protocols."""
    count = 10
    protocols = generate_protocols(count)
    
    assert len(protocols) == count
    
    # All should be valid HTTP protocols
    for protocol in protocols:
        assert protocol in HTTP_PROTOCOLS

def test_empty_protocols():
    """Test generating zero HTTP protocols."""
    protocols = generate_protocols(0)
    assert protocols == []

def test_protocol_distribution():
    """Test that HTTP protocols follow realistic distribution."""
    count = 1000
    protocols = generate_protocols(count)
    
    # Count occurrences
    counter = Counter(protocols)
    
    # Check that all protocols are present
    assert set(counter.keys()) == set(HTTP_PROTOCOLS)
    
    # Check that HTTP/1.1 is most common (should be around 60%)
    http11_percentage = counter["HTTP/1.1"] / count
    assert 0.5 < http11_percentage < 0.7  # Allow some variance
    
    # Check that HTTP/2 is second most common (should be around 35%)
    http2_percentage = counter["HTTP/2"] / count
    assert 0.25 < http2_percentage < 0.45  # Allow some variance
    
    # Check that HTTP/1.1 is more common than HTTP/2
    assert counter["HTTP/1.1"] > counter["HTTP/2"]
    
    # Check that HTTP/2 is more common than HTTP/3
    assert counter["HTTP/2"] > counter["HTTP/3"]

def test_protocol_values():
    """Test that generated values are valid HTTP protocols."""
    protocol = generate_protocol()
    
    valid_protocols = {"HTTP/1.1", "HTTP/2", "HTTP/3"}
    assert protocol in valid_protocols

def test_protocol_format():
    """Test that protocols follow proper HTTP format."""
    protocol = generate_protocol()
    
    # Should start with HTTP/
    assert protocol.startswith("HTTP/")
    
    # Should have version number
    version = protocol.split("/")[1]
    assert version in ["1.1", "2", "3"]

# Path tests
def test_generate_path():
    """Test single API path generation."""
    path = generate_path()
    
    # Check format
    assert isinstance(path, str)
    assert path.startswith("/api/v1/")
    
    # Should be a valid API path
    assert any(path.startswith(p.replace("{id}", "")) for p in API_PATHS)

def test_generate_paths():
    """Test generating multiple API paths."""
    count = 10
    paths = generate_paths(count)
    
    assert len(paths) == count
    
    # All should be valid API paths
    for path in paths:
        assert path.startswith("/api/v1/")

def test_empty_paths():
    """Test generating zero API paths."""
    paths = generate_paths(0)
    assert paths == []

def test_path_distribution():
    """Test that API paths follow realistic distribution."""
    count = 1000
    paths = generate_paths(count)
    
    # Count occurrences of base paths (without IDs)
    base_paths = []
    for path in paths:
        # Extract base path without ID
        if "/users/" in path and path != "/api/v1/users":
            base_paths.append("/api/v1/users/{id}")
        elif "/posts/" in path and path != "/api/v1/posts":
            base_paths.append("/api/v1/posts/{id}")
        elif "/comments/" in path and path != "/api/v1/comments":
            base_paths.append("/api/v1/comments/{id}")
        else:
            base_paths.append(path)
    
    counter = Counter(base_paths)
    
    # Check that users endpoints are most common
    users_count = counter.get("/api/v1/users", 0) + counter.get("/api/v1/users/{id}", 0)
    posts_count = counter.get("/api/v1/posts", 0) + counter.get("/api/v1/posts/{id}", 0)
    
    assert users_count > posts_count

def test_id_replacement():
    """Test that {id} placeholders are replaced with realistic IDs."""
    count = 100
    paths = generate_paths(count)
    
    # Find paths with IDs
    id_paths = [path for path in paths if any(pattern in path for pattern in ["/users/", "/posts/", "/comments/"])]
    
    if id_paths:  # Should have some ID paths
        for path in id_paths:
            # Should not contain {id} placeholder
            assert "{id}" not in path
            
            # Should have some ID after the resource
            parts = path.split("/")
            assert len(parts) >= 4  # /api/v1/resource/id
            
            # ID should be at the end
            id_part = parts[-1]
            assert id_part  # Should not be empty

def test_id_patterns():
    """Test that IDs follow realistic patterns."""
    count = 200
    paths = generate_paths(count)
    
    # Find paths with IDs
    id_paths = [path for path in paths if any(pattern in path for pattern in ["/users/", "/posts/", "/comments/"])]
    
    if id_paths:
        for path in id_paths:
            id_part = path.split("/")[-1]
            
            # ID should be one of: number, UUID, or slug
            is_number = id_part.isdigit()
            is_uuid = bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', id_part))
            is_slug = bool(re.match(r'^[a-z0-9-]+$', id_part))
            
            assert is_number or is_uuid or is_slug, f"Invalid ID format: {id_part}"

def test_path_structure():
    """Test that all paths follow proper API structure."""
    count = 50
    paths = generate_paths(count)
    
    for path in paths:
        # Should start with /api/v1/
        assert path.startswith("/api/v1/")
        
        # Should not have double slashes (except for /api/v1/)
        assert "//" not in path[7:]  # After /api/v1/
        
        # Should not end with slash (except for root paths)
        if path != "/api/v1/":
            assert not path.endswith("/")

# Query parameters tests
def test_generate_query_parameters():
    """Test single query parameters generation."""
    params = generate_query_parameters()
    
    # Check format
    assert isinstance(params, str)
    
    # Should be empty or start with ?
    if params:
        assert params.startswith("?")

def test_generate_query_parameters_list():
    """Test generating multiple query parameters."""
    count = 10
    params_list = generate_query_parameters_list(count)
    
    assert len(params_list) == count
    
    # All should be strings
    for params in params_list:
        assert isinstance(params, str)

def test_empty_query_parameters():
    """Test generating zero query parameters."""
    params_list = generate_query_parameters_list(0)
    assert params_list == []

def test_query_parameters_distribution():
    """Test that query parameters follow realistic distribution."""
    count = 1000
    params_list = generate_query_parameters_list(count)
    
    # Count empty vs non-empty
    empty_count = sum(1 for p in params_list if p == "")
    non_empty_count = count - empty_count
    
    # Should have some empty (around 40%) and some with parameters (around 60%)
    empty_percentage = empty_count / count
    assert 0.3 < empty_percentage < 0.5  # Allow some variance
    
    # Non-empty should start with ?
    for params in params_list:
        if params:
            assert params.startswith("?")

def test_pagination_parameters():
    """Test that pagination parameters are valid."""
    count = 100
    params_list = generate_query_parameters_list(count)
    
    # Find pagination parameters
    pagination_params = [p for p in params_list if p and any(param in p for param in ["page=", "limit=", "offset="])]
    
    if pagination_params:
        for params in pagination_params:
            # Should contain pagination keywords
            assert any(keyword in params for keyword in ["page=", "limit=", "offset="])
            # Should be valid format
            assert "&" in params or "=" in params

def test_filtering_parameters():
    """Test that filtering parameters are valid."""
    count = 100
    params_list = generate_query_parameters_list(count)
    
    # Find filtering parameters
    filtering_params = [p for p in params_list if p and any(param in p for param in ["status=", "category=", "user_id=", "created_after="])]
    
    if filtering_params:
        for params in filtering_params:
            # Should contain filtering keywords
            assert any(keyword in params for keyword in ["status=", "category=", "user_id=", "created_after="])
            # Should be valid format
            assert "=" in params

def test_sorting_parameters():
    """Test that sorting parameters are valid."""
    count = 100
    params_list = generate_query_parameters_list(count)
    
    # Find sorting parameters
    sorting_params = [p for p in params_list if p and any(param in p for param in ["sort=", "order=", "sort_by=", "sort_order="])]
    
    if sorting_params:
        for params in sorting_params:
            # Should contain sorting keywords
            assert any(keyword in params for keyword in ["sort=", "order=", "sort_by=", "sort_order="])
            # Should be valid format
            assert "=" in params

def test_search_parameters():
    """Test that search parameters are valid."""
    count = 100
    params_list = generate_query_parameters_list(count)
    
    # Find search parameters
    search_params = [p for p in params_list if p and any(param in p for param in ["q=", "search=", "query="])]
    
    if search_params:
        for params in search_params:
            # Should contain search keywords
            assert any(keyword in params for keyword in ["q=", "search=", "query="])
            # Should be valid format
            assert "=" in params

def test_parameter_format():
    """Test that all parameters follow proper URL format."""
    count = 50
    params_list = generate_query_parameters_list(count)
    
    for params in params_list:
        if params:
            # Should start with ?
            assert params.startswith("?")
            
            # Should not have double ??
            assert "??" not in params
            
            # Should have key=value pairs
            if "=" in params:
                # Remove the leading ?
                param_string = params[1:]
                pairs = param_string.split("&")
                
                for pair in pairs:
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        assert key  # Key should not be empty
                        assert value  # Value should not be empty 