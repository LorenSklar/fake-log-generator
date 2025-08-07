"""
Configuration settings for fake log generator.
"""

from datetime import datetime, timedelta, timezone

# Default date range (3 years ago to now)
DEFAULT_START_DATE = datetime.now(timezone.utc) - timedelta(days=3 * 365)
DEFAULT_END_DATE = datetime.now(timezone.utc)

# Default output settings
DEFAULT_FORMAT = "json"
DEFAULT_OUTPUT_FILE = None  # stdout by default

# Default generation settings
DEFAULT_COUNT = 100

# Supported output formats
SUPPORTED_FORMATS = ["json", "csv", "log"]

# File extensions for each format
FORMAT_EXTENSIONS = {
    "json": ".json",
    "csv": ".csv", 
    "log": ".log"
}

# Default service configuration
DEFAULT_SERVICE_NAME = "api-service"
DEFAULT_ENVIRONMENT = "production"

# Performance settings
BATCH_SIZE = 1000  # Generate in batches for large counts 