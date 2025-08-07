# Fake Log Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Tests](https://github.com/yourusername/fake_log_generator/workflows/CI/badge.svg)](https://github.com/yourusername/fake_log_generator/actions)
[![Codecov](https://codecov.io/gh/yourusername/fake_log_generator/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/fake_log_generator)
[![PyPI](https://img.shields.io/pypi/v/fake-log-generator.svg)](https://pypi.org/project/fake-log-generator/)

A Python tool for generating realistic, fake log entries suitable for testing, development, and learning purposes. This generator creates web server log entries that mimic real-world HTTP request/response patterns.

## 🚀 Quick Start

```bash
# Generate 100 JSON log entries
python generate_logs.py 100

# Generate CSV for PostgreSQL import
python generate_logs.py 1000 --format csv --output logs.csv

# Generate traditional log format
python generate_logs.py 500 --format log --output app.log
```

## ✨ Features

- **Realistic Data**: Generates plausible log entries using Python's Faker library
- **Multiple Formats**: JSON, CSV, and traditional log output
- **CLI Interface**: Easy-to-use command-line tool
- **Comprehensive Fields**: All essential web server log fields
- **Scalable Output**: Generate from 100 to 100,000+ log entries
- **PostgreSQL Ready**: Optimized for database ingestion
- **GraphQL Learning**: Perfect foundation for GraphQL API development

## How This Fits Into the Larger GraphQL Project

This fake log generator is the **data foundation** for a comprehensive GraphQL learning system:

1. **Data Generation Phase** (Current) - Generate realistic log entries
2. **Database Integration** - Load generated data into PostgreSQL
3. **GraphQL Schema Design** - Create queries for log analysis
4. **API Development** - Build GraphQL endpoints with Ariadne
5. **Performance Testing** - Query datasets from 100 to 100,000+ records
6. **Real-world Scenarios** - Demonstrate log analysis, filtering, and aggregation

The generated logs will be used to practice complex GraphQL queries, demonstrate performance at scale, and show understanding of real-world data patterns.

## Features

- **Realistic Data**: Generates plausible log entries using Python's Faker library
- **Comprehensive Fields**: Includes all essential web server log fields
- **Scalable Output**: Generate from 100 to 100,000+ log entries
- **CSV Export**: Optimized for PostgreSQL database ingestion
- **Configurable**: Customize log patterns, error rates, and data distributions

## Log Entry Fields

Each log entry contains the following fields in logical order:

### Core Request Information
- **TIMESTAMP**: ISO 8601 formatted date and time represented as a string
- **REQUEST_ID**: Unique identifier for request-response tracing
- **METHOD**: HTTP method (GET, POST, PUT, DELETE, etc.)
- **PATH**: Requested URL path
- **QUERY_PARAMETERS**: URL query string parameters
- **PROTOCOL**: HTTP protocol version

### Client Information
- **SOURCE_IP**: Client IP address
- **USER_AGENT**: Browser/client information
- **REFERER**: Referring URL
- **USER_ID**: Authenticated user identifier
- **SESSION_ID**: Session identifier

### Request Details
- **REQUEST_HEADERS**: HTTP request headers (JSON format)
- **REQUEST_BODY**: Request payload content
- **CONTENT_LENGTH**: Size of request body

### Response Information
- **STATUS_CODE**: HTTP response status code
- **RESPONSE_TIME_MS**: Request processing time in milliseconds
- **RESPONSE_HEADERS**: HTTP response headers (JSON format)
- **RESPONSE_BODY**: Response content

### Logging Metadata
- **LOG_LEVEL**: Severity level (INFO, DEBUG, WARN, ERROR)
- **SERVICE_NAME**: Name of the service generating the log
- **ENV**: Environment (prod, staging, dev, test)

### Error Information (when LOG_LEVEL=ERROR)
- **ERROR_MESSAGE**: Descriptive error message
- **STACK_TRACE**: Error stack trace (truncated)

## Getting Started

### Quick Start

Generate fake log entries with a single command:

```bash
# Generate 100 JSON log entries to stdout
python generate_logs.py 100

# Generate 1000 CSV log entries to file
python generate_logs.py 1000 --format csv --output logs.csv

# Generate 500 log entries in traditional format
python generate_logs.py 500 --format log
```

### CLI Options

```bash
python generate_logs.py [COUNT] [OPTIONS]

Options:
  --format, -f     Output format: json, csv, log (default: json)
  --output, -o     Output file path (default: stdout)
  --start-date     Start date for logs (YYYY-MM-DD format)
  --end-date       End date for logs (YYYY-MM-DD format)
  --quiet, -q      Suppress progress output
```

### Examples

```bash
# Generate logs for a specific date range
python generate_logs.py 100 --start-date 2024-01-01 --end-date 2024-01-31

# Generate CSV logs for PostgreSQL import
python generate_logs.py 10000 --format csv --output production_logs.csv

# Generate traditional log format for log analysis
python generate_logs.py 500 --format log --output app.log

# Generate logs quietly (no progress output)
python generate_logs.py 1000 --quiet
```

## Programmatic Usage

### Generate Complete Log Entries

```python
from generators.log_entry_factory import generate_log_entry, generate_log_entries

# Generate a single complete log entry
log_entry = generate_log_entry()
print(log_entry)

# Generate multiple log entries
log_entries = generate_log_entries(100)
```

### Generate Formatted Log Lines

```python
from generators.log_entry_factory import generate_log_lines

# Generate JSON log lines
json_lines = generate_log_lines(100, "json")

# Generate CSV log lines
csv_lines = generate_log_lines(100, "csv")

# Generate traditional log lines
log_lines = generate_log_lines(100, "log")
```

### Individual Field Generation

```python
from generators.core_generators import generate_timestamp, generate_request_id
from generators.client_generators import generate_source_ip

# Generate individual fields
timestamp = generate_timestamp()
request_id = generate_request_id()
source_ip = generate_source_ip()

print(f"Timestamp: {timestamp}")
print(f"Request ID: {request_id}")
print(f"Source IP: {source_ip}")
```

### Generate Multiple Values

```python
from generators.core_generators import generate_timestamps, generate_log_levels

# Generate multiple timestamps (sorted chronologically)
timestamps = generate_timestamps(100)

# Generate multiple log levels with realistic distribution
log_levels = generate_log_levels(100)
```

### Export to CSV

```python
from generators.core_generators import generate_timestamps, generate_request_ids
from exporters.csv_exporter import export_to_csv

# Generate data
timestamps = generate_timestamps(100)
request_ids = generate_request_ids(100)

# Prepare data for export
data = [
    {"timestamp": ts, "request_id": rid} 
    for ts, rid in zip(timestamps, request_ids)
]

# Export to CSV
export_to_csv(data, "logs.csv", ["timestamp", "request_id"])
```

### PostgreSQL Integration

```python
from exporters.postgres_exporter import get_postgres_create_table_sql, generate_insert_values

# Get SQL to create the table
create_sql = get_postgres_create_table_sql()
print(create_sql)

# Generate insert values
data = [{"timestamp": ts, "request_id": rid} for ts, rid in zip(timestamps, request_ids)]
values = generate_insert_values(data, ["timestamp", "request_id"])
```

## Output Format

The generator exports log entries in CSV format, optimized for PostgreSQL ingestion:

```csv
TIMESTAMP,REQUEST_ID,METHOD,PATH,QUERY_PARAMETERS,PROTOCOL,SOURCE_IP,USER_AGENT,REFERER,USER_ID,SESSION_ID,REQUEST_HEADERS,REQUEST_BODY,CONTENT_LENGTH,STATUS_CODE,RESPONSE_TIME_MS,RESPONSE_HEADERS,RESPONSE_BODY,LOG_LEVEL,SERVICE_NAME,ENV,ERROR_MESSAGE,STACK_TRACE
2024-01-15T10:30:45.123Z,req_12345,GET,/api/users,{"page":"1","limit":"10"},HTTP/1.1,192.168.1.100,Mozilla/5.0...,https://example.com,user_123,sess_456,{"Accept":"application/json"},,0,200,45,{"Content-Type":"application/json"},{"users":[...]},INFO,user-service,prod,,
```

## Data Realism

The generator creates realistic patterns including:
- **Realistic IP ranges**: Mix of local, private, and public IPs
- **Common HTTP paths**: API endpoints, static resources, admin pages
- **Status code distribution**: Mostly 200s, some 4xx/5xx errors
- **Response time patterns**: Fast for static content, slower for complex operations
- **User agent variety**: Different browsers, mobile devices, bots
- **Error scenarios**: Network timeouts, validation errors, server errors

## PostgreSQL Integration

The CSV output is designed for easy PostgreSQL ingestion:

Note: CSV contains timestamp as ISO 8601 string, PostgreSQL converts to timestamptz

```sql
-- Create table
CREATE TABLE log_entries (
    timestamp TIMESTAMPTZ,
    request_id VARCHAR(50),
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

-- Import CSV
COPY log_entries FROM '/path/to/logs.csv' WITH (FORMAT csv, HEADER true);
```

## Development Roadmap

### Phase 1: Data Generation ✅ (Complete)
- [x] Timestamp generator with realistic date ranges
- [x] Request ID generator with UUIDs
- [x] Log level generator (INFO, DEBUG, WARN, ERROR with realistic distribution)
- [x] HTTP method generator (GET, POST, PUT, DELETE with API-focused distribution)
- [x] HTTP protocol generator (HTTP/1.1, HTTP/2, HTTP/3)
- [x] Path generator (API endpoints with dynamic ID replacement)
- [x] Query parameters generator (pagination, filtering, sorting, search)
- [x] IP address generator (mix of IPv4, IPv6, private IPs)
- [x] User agent generator (browsers, mobile, bots)
- [x] Referer generator (URLs and empty values)
- [x] User ID generator (UUIDs, usernames, emails)
- [x] Session ID generator (UUIDs, hex strings)
- [x] Log entry factory (combines all generators)
- [x] CLI script for easy generation
- [x] Multiple output formats (JSON, CSV, traditional log)

### Phase 2: Data Export & Database ✅ (Complete)
- [x] CSV export functionality
- [x] PostgreSQL table creation scripts
- [x] Data loading utilities
- [x] Configuration system
- [x] Performance testing ready

### Phase 3: GraphQL Implementation (Next)
- [ ] Status code generator (200, 404, 500, etc. with realistic ratios)
- [ ] Response time generator (realistic processing times)
- [ ] Request/response headers and body generators
- [ ] Service name and environment generators
- [ ] Error message and stack trace generators
- [ ] GraphQL schema design for log queries
- [ ] Ariadne-based API development
- [ ] Query resolvers for filtering and aggregation
- [ ] Performance optimization for large datasets

### Scaling Goals
- [x] Generate 100 log entries for initial testing
- [ ] Scale to 1,000 entries for performance testing
- [ ] Scale to 10,000 entries for stress testing
- [ ] Scale to 100,000+ entries for production-like datasets
- [ ] Add GraphQL endpoint for querying generated logs

## Requirements

- Python 3.8+
- Faker library
- pandas (for CSV handling)

## Installation

```bash
pip install faker pandas
```

## Maintenance Guide

When adding new log entry fields, update these files to maintain consistency:

### Core Files to Update

1. **`generators/log_entry_factory.py`**
   - Add new field to `generate_log_entry()` function
   - Update placeholder values for new fields
   - Add TODO comment for future generator implementation

2. **`exporters/csv_exporter.py`**
   - Update `convert_to_csv_value()` if new field type needs special handling
   - Test with new field types

3. **`exporters/postgres_exporter.py`**
   - Update `get_postgres_create_table_sql()` with new column
   - Update `get_postgres_insert_sql()` with new placeholder
   - Update `convert_to_postgres_value()` if new field type needs special handling
   - Test with new field types

4. **`tests/test_csv_exporter.py`**
   - Add test for new field type conversion
   - Test export with new fields

5. **`tests/test_postgres_exporter.py`**
   - Add test for new field type conversion
   - Test SQL generation with new fields

6. **`tests/test_log_entry_factory.py`**
   - Add new field to `required_fields` list in `test_generate_log_entry()`
   - Add data type assertion for new field
   - Test formatting with new field

### Optional Updates

7. **`config.py`**
   - Add default values for new fields if needed
   - Update constants if new field affects configuration

8. **`rules.md`**
   - Add patterns for new field types
   - Update data patterns section if new field has specific requirements

### Example: Adding a New Field

```python
# 1. Add to log_entry_factory.py
def generate_log_entry() -> Dict[str, Any]:
    # ... existing code ...
    
    log_entry = {
        # ... existing fields ...
        "new_field": "placeholder_value",  # TODO: implement new_field_generator
    }
    
    return log_entry

# 2. Update postgres_exporter.py
def get_postgres_create_table_sql() -> str:
    return """
    CREATE TABLE IF NOT EXISTS log_entries (
        -- ... existing columns ...
        new_field VARCHAR(100),  -- Add new column
    );
    """

# 3. Update tests
def test_generate_log_entry():
    required_fields = [
        # ... existing fields ...
        "new_field",  # Add to required fields
    ]
    
    # Add data type assertion
    assert isinstance(log_entry["new_field"], str)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 **Report bugs** - Help us improve by reporting issues
- 💡 **Suggest features** - Share ideas for new functionality
- 🔧 **Fix bugs** - Submit pull requests for bug fixes
- ✨ **Add features** - Implement new generators or exporters
- 📚 **Improve docs** - Help make the documentation better
- 🧪 **Write tests** - Add test coverage for new features

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📊 Project Status

- **Phase 1**: ✅ Complete - Core generators and CLI
- **Phase 2**: ✅ Complete - Export functionality and configuration
- **Phase 3**: 🚧 In Progress - GraphQL implementation

## 🎯 Roadmap

- [ ] Status code generator with realistic distribution
- [ ] Response time generator with performance patterns
- [ ] Request/response headers and body generators
- [ ] GraphQL schema and API implementation
- [ ] Performance testing at scale (100k+ records)
- [ ] Docker containerization
- [ ] PyPI package distribution

## 📈 Getting Stars and Followers

If you find this project useful, please consider:

- ⭐ **Star the repository** - Shows appreciation and helps with visibility
- 👀 **Watch the repository** - Stay updated with new features and releases
- 🔄 **Fork the repository** - Create your own version or contribute back
- 💬 **Open issues** - Report bugs or suggest improvements
- 📢 **Share with others** - Tell your network about this project
- 🐛 **Contribute code** - Submit pull requests for improvements

### Why Star This Project?

- **Learning Resource**: Perfect for learning GraphQL with realistic data
- **Development Tool**: Generate test data for any web application
- **Open Source**: Free to use, modify, and distribute
- **Active Development**: Regular updates and improvements
- **Community Driven**: Built with input from the developer community

## 📄 License

Creative Commons Attribution 4.0 International License (CC BY 4.0)

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

**Under the following terms:**
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

This project is designed for learning and development purposes. Feel free to use, modify, and share!

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/fake_log_generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fake_log_generator/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for security contact information 