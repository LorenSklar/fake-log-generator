"""
Log level generator for fake log entries.
"""

import random

LOG_LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
LOG_LEVEL_WEIGHTS = [70, 15, 10, 5]  

def generate_log_level() -> str:
    """Return a single log level with realistic distribution."""
    return random.choices(LOG_LEVELS, weights=LOG_LEVEL_WEIGHTS)[0]

def generate_log_levels(count: int) -> list[str]:
    """Return a list of log levels with realistic distribution."""
    return [generate_log_level() for _ in range(count)] 