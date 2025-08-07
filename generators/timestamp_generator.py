"""
Simple timestamp generator for fake log entries.
"""

from datetime import datetime, timedelta, timezone
from faker import Faker

DEFAULT_START_DATE = datetime.now(timezone.utc) - timedelta(days=3 * 365)
DEFAULT_END_DATE = datetime.now(timezone.utc)

fake = Faker()

def generate_timestamp(start_date: datetime = DEFAULT_START_DATE, end_date: datetime = DEFAULT_END_DATE) -> datetime:
    """Return a single UTC timestamp as datetime object."""
    if end_date < start_date:
        raise ValueError(f"end_date ({end_date}) cannot be before start_date ({start_date})")
    
    timestamp = fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=timezone.utc)
    return timestamp

def generate_timestamps(count: int, start_date: datetime = DEFAULT_START_DATE, end_date: datetime = DEFAULT_END_DATE, sort: bool = True) -> list[datetime]:
    """Return a list of UTC timestamps as datetime objects."""
    if end_date < start_date:
        raise ValueError(f"end_date ({end_date}) cannot be before start_date ({start_date})")
    
    timestamps = [generate_timestamp(start_date, end_date) for _ in range(count)]
    if sort:
        timestamps.sort()
    return timestamps

