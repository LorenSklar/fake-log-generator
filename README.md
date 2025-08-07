# Fake Log Generator

A Python tool for generating realistic, fake log entries suitable for testing, development, and learning purposes. This generator creates web server log entries that mimic real-world HTTP request/response patterns.

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

## Usage

```bash
# Generate 100 log entries
python fake_log_generator.py --count 100

# Generate 1000 log entries with custom error rate
python fake_log_generator.py --count 1000 --error-rate 0.05

# Generate logs for specific service
python fake_log_generator.py --count 500 --service api-gateway

# Export to specific file
python fake_log_generator.py --count 10000 --output large_dataset.csv
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

### Phase 1: Data Generation (Current)
- [x] Timestamp generator with realistic date ranges
- [x] Request ID generator with UUIDs
- [ ] Log level generator (INFO, DEBUG, WARN, ERROR with realistic distribution)
- [ ] HTTP method generator (GET, POST, PUT, DELETE, etc.)
- [ ] Status code generator (200, 404, 500, etc. with realistic ratios)
- [ ] IP address generator (mix of local, private, public IPs)
- [ ] User agent generator (browsers, mobile, bots)
- [ ] Path generator (API endpoints, static resources, admin pages)
- [ ] Response time generator (realistic processing times)
- [ ] Log entry factory (combines all generators)

### Phase 2: Data Export & Database
- [ ] CSV export functionality
- [ ] PostgreSQL table creation scripts
- [ ] Data loading utilities
- [ ] Performance testing (100 → 1,000 → 10,000 → 100,000 records)

### Phase 3: GraphQL Implementation
- [ ] GraphQL schema design for log queries
- [ ] Ariadne-based API development
- [ ] Query resolvers for filtering and aggregation
- [ ] Performance optimization for large datasets

- [ ] Generate 100 log entries for initial testing
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

## License

MIT License - feel free to use for learning and development purposes. 