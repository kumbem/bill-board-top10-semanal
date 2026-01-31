from datetime import datetime, timedelta

def iter_week_dates(start: datetime, end: datetime):
    """Yield weekly dates from start to end (inclusive)."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=7)
