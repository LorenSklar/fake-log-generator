"""
Log entry factory for assembling complete fake log entries.
"""

import json
from datetime import datetime
from typing import Dict, Any

from generators.core_generators import (
    generate_timestamp, generate_request_id, generate_log_level,
    generate_method, generate_path, generate_query_parameters,
    generate_protocol
)
from generators.client_generators import (
    generate_source_ip, generate_user_agent, generate_referer,
    generate_user_id, generate_session_id
)

def generate_log_entry() -> Dict[str, Any]:
    """Generate a single complete log entry as a dictionary.
    
    Returns:
        Dictionary containing all log entry fields with realistic values
    """
    # Generate core fields
    timestamp = generate_timestamp()
    request_id = generate_request_id()
    log_level = generate_log_level()
    method = generate_method()
    path = generate_path()
    query_params = generate_query_parameters()
    protocol = generate_protocol()
    
    # Generate client information
    source_ip = generate_source_ip()
    user_agent = generate_user_agent()
    referer = generate_referer()
    user_id = generate_user_id()
    session_id = generate_session_id()
    
    # Assemble the log entry
    log_entry = {
        "timestamp": timestamp,
        "log_level": log_level,
        "request_id": request_id,
        "source_ip": source_ip,
        "method": method,
        "path": path,
        "query_parameters": query_params,
        "protocol": protocol,
        "user_agent": user_agent,
        "referer": referer,
        "user_id": user_id,
        "session_id": session_id,
        # Placeholder fields for future implementation
        "status_code": 200,  # TODO: implement status_code_generator
        "response_time_ms": 150,  # TODO: implement response_time_generator
        "request_headers": {},  # TODO: implement request_headers_generator
        "request_body": "",  # TODO: implement request_body_generator
        "response_headers": {},  # TODO: implement response_headers_generator
        "response_body": "",  # TODO: implement response_body_generator
        "service_name": "api-service",  # TODO: implement service_name_generator
        "env": "production",  # TODO: implement env_generator
        "error_message": "",  # TODO: implement error_message_generator
        "stack_trace": ""  # TODO: implement stack_trace_generator
    }
    
    return log_entry

def generate_log_entries(count: int) -> list[Dict[str, Any]]:
    """Generate multiple complete log entries.
    
    Args:
        count: Number of log entries to generate
        
    Returns:
        List of log entry dictionaries
    """
    return [generate_log_entry() for _ in range(count)]

def format_log_entry_as_string(log_entry: Dict[str, Any], format_type: str = "json") -> str:
    """Format a log entry as a string.
    
    Args:
        log_entry: Log entry dictionary
        format_type: Output format ("json", "csv", "log")
        
    Returns:
        Formatted log entry string
    """
    if format_type == "json":
        # Convert datetime to ISO string for JSON serialization
        entry_copy = log_entry.copy()
        entry_copy["timestamp"] = log_entry["timestamp"].isoformat()
        entry_copy["request_id"] = str(log_entry["request_id"])
        return json.dumps(entry_copy)
    
    elif format_type == "csv":
        # Simple CSV format (timestamp,log_level,request_id,source_ip,method,path,status_code)
        timestamp_str = log_entry["timestamp"].isoformat()
        request_id_str = str(log_entry["request_id"])
        return f"{timestamp_str},{log_entry['log_level']},{request_id_str},{log_entry['source_ip']},{log_entry['method']},{log_entry['path']},{log_entry['status_code']}"
    
    elif format_type == "log":
        # Traditional log format
        timestamp_str = log_entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        request_id_str = str(log_entry["request_id"])
        return f"{timestamp_str} [{log_entry['log_level']}] {request_id_str} {log_entry['source_ip']} {log_entry['method']} {log_entry['path']} {log_entry['status_code']}"
    
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

def generate_log_lines(count: int, format_type: str = "json") -> list[str]:
    """Generate multiple formatted log entry strings.
    
    Args:
        count: Number of log entries to generate
        format_type: Output format ("json", "csv", "log")
        
    Returns:
        List of formatted log entry strings
    """
    log_entries = generate_log_entries(count)
    return [format_log_entry_as_string(entry, format_type) for entry in log_entries] 