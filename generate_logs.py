#!/usr/bin/env python3
"""
CLI script to generate fake log entries.
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from generators.log_entry_factory import generate_log_lines, generate_log_entries
from exporters.csv_exporter import export_to_csv

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate fake log entries for testing and development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 100 JSON log entries to stdout
  python generate_logs.py 100

  # Generate 1000 CSV log entries to file
  python generate_logs.py 1000 --format csv --output logs.csv

  # Generate 500 log entries in traditional format
  python generate_logs.py 500 --format log

  # Generate logs with custom date range
  python generate_logs.py 100 --start-date 2024-01-01 --end-date 2024-01-31
        """
    )
    
    parser.add_argument(
        "count",
        type=int,
        help="Number of log entries to generate"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["json", "csv", "log"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date for log entries (YYYY-MM-DD format, default: 3 years ago)"
    )
    
    parser.add_argument(
        "--end-date",
        type=str,
        help="End date for log entries (YYYY-MM-DD format, default: now)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    return parser.parse_args()

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD format.")

def main():
    """Main CLI function."""
    args = parse_args()
    
    # Validate count
    if args.count <= 0:
        print("Error: Count must be a positive integer", file=sys.stderr)
        sys.exit(1)
    
    # Parse dates if provided
    start_date = None
    end_date = None
    
    if args.start_date:
        try:
            start_date = parse_date(args.start_date)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.end_date:
        try:
            end_date = parse_date(args.end_date)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Validate date range
    if start_date and end_date and end_date <= start_date:
        print("Error: End date must be after start date", file=sys.stderr)
        sys.exit(1)
    
    # Show progress
    if not args.quiet:
        print(f"Generating {args.count} log entries in {args.format.upper()} format...", file=sys.stderr)
        if start_date:
            print(f"Start date: {start_date.date()}", file=sys.stderr)
        if end_date:
            print(f"End date: {end_date.date()}", file=sys.stderr)
    
    try:
        # Handle CSV format specially to include headers
        if args.format == "csv":
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Generate log entries and export to CSV with headers
                log_entries = generate_log_entries(args.count)
                export_to_csv(log_entries, str(output_path))
                
                if not args.quiet:
                    print(f"Generated {len(log_entries)} log entries to {output_path}", file=sys.stderr)
            else:
                # For CSV to stdout, we need to use the CSV exporter
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
                    log_entries = generate_log_entries(args.count)
                    export_to_csv(log_entries, tmp_file.name)
                
                # Read and output the CSV content
                with open(tmp_file.name, 'r') as f:
                    print(f.read(), end='')
                
                # Clean up temp file
                import os
                os.unlink(tmp_file.name)
        else:
            # Generate log lines for other formats
            log_lines = generate_log_lines(args.count, args.format)
            
            # Output to file or stdout
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    for line in log_lines:
                        f.write(line + '\n')
                
                if not args.quiet:
                    print(f"Generated {len(log_lines)} log entries to {output_path}", file=sys.stderr)
            else:
                # Output to stdout
                for line in log_lines:
                    print(line)
    
    except Exception as e:
        print(f"Error generating log entries: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 