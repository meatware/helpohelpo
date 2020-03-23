"""Helpers to manipulate times"""

import os
from datetime import datetime
import arrow

import sys
import os
import logging
from datetime import datetime, timedelta
import re
from dateutil import tz
from pydash import get

LOG = logging.getLogger(__name__)


def get_unix_ts_unit(unix_ts):
    """Check if linux timestamp units are in seconds or ms."""

    if len(unix_ts) == 13:
        unit = "ms"
    elif len(unix_ts) == 10:
        unit = "s"
    return unit


def convert_unix_time(unix_time):
    """Convert unix timestamp to date-time object."""

    return datetime.fromtimestamp(unix_time / 1000, tz=tz.tzutc())


def format_dt_object(dt_obj, fmt_str):
    """return date time object in format specified."""

    return datetime.strftime(dt_obj, fmt_str)


def check_date_fmt(date_string=None):
    """Check that date matches format "YYYY-MM-DD"."""

    if re.match(REGEX_PATTERN, date_string):
        LOG.debug("date string verified")
        return True

    LOG.debug("Whoops! Incorrect date format")

    return False


def string_to_datetime(date_str, time_format):
    """Convert pre-checked string into datetime object."""

    datet_obj = datetime.strptime(date_str, time_format)

    return datet_obj


def calc_ndays_fwd(ndays):
    """Returns a date string n days from today for use in
    an AWS schedule_deletion tag."""

    utc_time_now = datetime.utcnow()
    ndays_fwd = utc_time_now.date() + timedelta(days=ndays)
    ndays_fwd_str = format_dt_object(ndays_fwd, "%Y-%m-%d")

    return ndays_fwd_str


def calc_ndays_back_from_today(days_back):
    """Calculates the difference bewteen today and ndays back."""

    utc_time_now = datetime.utcnow().replace(tzinfo=tz.tzutc())
    ndays_back = utc_time_now - timedelta(days=days_back)
    return ndays_back


def calc_days_from_2dates_diff(prev_date):
    """Calculates the difference bewteen today and a previous date in days."""

    utc_time_now = datetime.utcnow().replace(tzinfo=tz.tzutc())
    # ndays_back = utc_time_now - timedelta(days=prev_date)
    ndays_back = utc_time_now - prev_date
    return ndays_back.days


def datetimeformat(date_str):
    """Print relative time from date_str."""

    mydate_time = arrow.get(date_str)
    return mydate_time.humanize()


def unixtime_to_datestring(unix_time):
    """Convert unix timestamp into a string."""

    return datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")


def unixtime_to_datetime(unix_time):
    """Convert unix timestamp into a string."""

    return datetime.utcfromtimestamp(unix_time)


# TODO: unify redundant time functions
def time_from_string(mytime_str, tformat="%H:%M"):
    """Converts a string into a time object."""
    return datetime.strptime(mytime_str, tformat).time()


def date_from_string(mydate_str):
    """Converts a string into a date object."""
    return datetime.strptime(mydate_str, "%Y-%m-%d").date()


# TODO: Move to another module
def find_nested_key(aws_response, key_path):
    """Check if nested mixed dictionary/list object has dict key. Uses pydash get"""

    return get(aws_response, key_path)
