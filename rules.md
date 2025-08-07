# Project Rules & Guidelines

## Code Style & Architecture

### Generators
- **Single purpose functions** - each generator does one thing well
- **Native types** - return most efficient format (datetime objects, UUID objects, etc.)
- **Type hints** - use them for clarity and IDE support
- **No over-engineering** - avoid classes, keep it simple
- **Consistent patterns** - `generate_single()` and `generate_multiple(count)` functions
- **Realistic defaults** - sensible defaults that mimic real-world data

### Export Layer
- **Separation of concerns** - generators return native types, exporters handle formatting
- **CSV export** - converts everything to strings for file output
- **PostgreSQL export** - preserves native types for database insertion
- **Flexible** - can easily add other export formats

### Testing
- **Comprehensive coverage** - test format, distribution, edge cases
- **Realistic validation** - test that data follows expected patterns
- **Edge cases** - empty lists, missing fields, invalid inputs
- **Performance** - test with larger datasets when relevant
- **Keep exporters updated** - update test_csv_exporter.py and test_postgres_exporter.py when adding new generators

## Data Patterns

### Timestamps
- **ISO 8601 format** - for CSV export (string)
- **UTC timezone** - all timestamps in UTC
- **Sortable** - chronological order with optional sort flag
- **Realistic ranges** - 3 years ago to now by default

### Request IDs
- **UUID format** - standard UUID with hyphens
- **Unique** - no duplicates when generating multiple
- **Native UUID objects** - for PostgreSQL compatibility

### Log Levels
- **Realistic distribution** - INFO (70%), WARN (15%), ERROR (10%), DEBUG (5%)
- **Weighted random** - use `random.choices()` with weights
- **Constants** - define LOG_LEVELS and LOG_LEVEL_WEIGHTS at top

### HTTP Methods
- **API-focused distribution** - POST (60%), GET (25%), PUT (10%), DELETE (5%)
- **Weighted random** - same pattern as log levels
- **API context** - POST dominates for data operations, GET for retrieval

### Status Codes
- **Realistic distribution** - 200 (80%), 404 (10%), 500 (5%), others (5%)
- **Dependent on log level** - ERROR logs typically have 4xx/5xx codes

## Project Structure

```
generators/
  timestamp_generator.py
  request_id_generator.py
  log_level_generator.py
  method_generator.py
  status_code_generator.py
  ...

exporters/
  csv_exporter.py
  postgres_exporter.py
  ...

tests/
  test_timestamp_generator.py
  test_request_id_generator.py
  test_log_level_generator.py
  ...

TEST_INSTRUCTIONS.md
```

## Dependencies

### Only import what you need
- **Faker** - only when actually using Faker functionality
- **Standard library** - prefer uuid, random, datetime over external libraries
- **Type hints** - use built-in types, no typing library imports

### Requirements
- `faker>=20.0.0` - for realistic data generation
- `pandas>=2.0.0` - for CSV handling (when needed)
- `pytest>=7.0.0` - for testing
- `pytest-cov>=4.0.0` - for coverage reporting

## GraphQL Integration

### Data Volume Planning
- **Scalable approach** - 100 → 1,000 → 10,000 → 100,000 records
- **Performance testing** - each scale level for query optimization
- **Realistic data** - patterns that mimic real-world logs

### Export Strategy
- **CSV for storage** - efficient file format for large datasets
- **PostgreSQL for queries** - native types for optimal performance
- **GraphQL schema** - designed for log analysis and filtering

## Common Patterns

### Weighted Random Selection
```python
OPTIONS = ["A", "B", "C"]
WEIGHTS = [70, 20, 10]
return random.choices(OPTIONS, weights=WEIGHTS)[0]
```

### Native Type Returns
```python
def generate_timestamp() -> datetime:
    return fake.date_time_between(...).replace(tzinfo=timezone.utc)

def generate_request_id() -> uuid.UUID:
    return uuid.uuid4()
```

### Export Conversion
```python
# CSV: convert to strings
datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# PostgreSQL: preserve native types
datetime_obj  # unchanged
uuid_obj      # unchanged
``` 