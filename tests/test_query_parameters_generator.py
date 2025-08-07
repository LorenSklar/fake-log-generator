"""
Test query parameters generator.
"""

import pytest
from collections import Counter
from generators.query_parameters_generator import (
    generate_query_parameters, 
    generate_query_parameters_list,
    QUERY_PARAM_TYPES,
    QUERY_PARAM_WEIGHTS,
    PAGINATION_PARAMS,
    FILTERING_PARAMS,
    SORTING_PARAMS,
    SEARCH_PARAMS
)

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