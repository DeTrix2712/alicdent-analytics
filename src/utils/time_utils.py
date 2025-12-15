# src/utils/time_utils.py
from datetime import datetime, timezone, date


def utc_now() -> datetime:
    """Текущее время в UTC."""
    return datetime.now(timezone.utc)


def to_date(dt: datetime | date) -> date:
    """Безопасно получить date из datetime/date."""
    if isinstance(dt, datetime):
        return dt.date()
    return dt
