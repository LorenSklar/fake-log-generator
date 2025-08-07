"""
CSV exporter for fake log entries.
"""

import csv
from datetime import datetime
from typing import Any, Dict, List

def convert_to_csv_value(value: Any) -> str:
    """Convert any value to CSV-compatible string."""
    if value is None:
        return ""
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    elif isinstance(value, (int, float, bool)):
        return str(value)
    else:
        return str(value)

def export_to_csv(data: List[Dict[str, Any]], filename: str, fieldnames: List[str] = None) -> None:
    """Export data to CSV file."""
    if not data:
        return
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            # Convert all values to CSV-compatible strings
            csv_row = {field: convert_to_csv_value(row.get(field, "")) for field in fieldnames}
            writer.writerow(csv_row) 