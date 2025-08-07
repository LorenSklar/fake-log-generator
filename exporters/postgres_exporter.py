"""
PostgreSQL exporter for fake log entries.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List

def get_postgres_create_table_sql() -> str:
    """Return SQL to create the log_entries table."""
    return """
CREATE TABLE IF NOT EXISTS log_entries (
    timestamp TIMESTAMPTZ NOT NULL,
    request_id UUID NOT NULL,
    method VARCHAR(10),
    path TEXT,
    query_parameters JSONB,
    protocol VARCHAR(10),
    source_ip INET,
    user_agent TEXT,
    referer TEXT,
    user_id VARCHAR(50),
    session_id VARCHAR(50),
    request_headers JSONB,
    request_body TEXT,
    content_length INTEGER,
    status_code INTEGER,
    response_time_ms INTEGER,
    response_headers JSONB,
    response_body TEXT,
    log_level VARCHAR(10),
    service_name VARCHAR(50),
    env VARCHAR(20),
    error_message TEXT,
    stack_trace TEXT
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_log_entries_timestamp ON log_entries(timestamp);
CREATE INDEX IF NOT EXISTS idx_log_entries_log_level ON log_entries(log_level);
CREATE INDEX IF NOT EXISTS idx_log_entries_status_code ON log_entries(status_code);
CREATE INDEX IF NOT EXISTS idx_log_entries_service_name ON log_entries(service_name);
"""

def get_postgres_insert_sql() -> str:
    """Return SQL template for inserting log entries."""
    return """
INSERT INTO log_entries (
    timestamp, request_id, method, path, query_parameters, protocol,
    source_ip, user_agent, referer, user_id, session_id, request_headers,
    request_body, content_length, status_code, response_time_ms,
    response_headers, response_body, log_level, service_name, env,
    error_message, stack_trace
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

def convert_to_postgres_value(value: Any) -> Any:
    """Convert value to PostgreSQL-compatible format."""
    if value is None:
        return None
    elif isinstance(value, datetime):
        return value  # PostgreSQL handles datetime objects
    elif isinstance(value, uuid.UUID):
        return value  # PostgreSQL handles UUID objects
    elif isinstance(value, (int, float, bool, str)):
        return value  # PostgreSQL handles these natively
    else:
        return str(value)  # Convert everything else to string

def generate_insert_values(data: List[Dict[str, Any]], fieldnames: List[str]) -> List[tuple]:
    """Convert data to list of tuples for PostgreSQL insertion."""
    values_list = []
    
    for row in data:
        values = []
        for field in fieldnames:
            value = row.get(field)
            values.append(convert_to_postgres_value(value))
        values_list.append(tuple(values))
    
    return values_list 