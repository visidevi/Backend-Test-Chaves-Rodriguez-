"""Time utilities."""
from backend_test.settings import APP_TZ, MAX_ORDER_HOUR
from datetime import datetime
import pytz


def get_datetime_for_custom_timezone(
        tz_string: str = APP_TZ,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0):
    """Get a datetime object for the custom timezone"""
    tz = pytz.timezone(tz_string)
    date = datetime.now(tz).replace(hour=hour, minute=minute,
                                    second=second, microsecond=microsecond)
    return date


def get_datetime_from_timestap(timestamp, tz_string=APP_TZ):
    """Get a datetime object from a timestamp"""
    utc_dt = datetime.utcfromtimestamp(timestamp)
    aware_utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    tz_custom = pytz.timezone(tz_string)
    dt = aware_utc_dt.astimezone(tz_custom)

    return dt


def get_local_timestamp_for_custom_hour(tz_string=APP_TZ, hour=MAX_ORDER_HOUR):
    """Get the timestamp of the next hour in the custom timezone"""
    tz_custom = pytz.timezone(tz_string)
    local_datetime = datetime.now(tz_custom).replace(
        hour=int(hour), minute=0, second=0, microsecond=0)
    response = datetime.timestamp(local_datetime)
    return response
