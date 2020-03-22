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

# import pandas as pd


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


def find_nested_key(aws_response, key_path):
    """Check if nested mixed dictionary/list object has dict key."""

    return get(aws_response, key_path)


def datetimeformat(date_str):
    """Print relative time from date_str."""

    mydate_time = arrow.get(date_str)
    return mydate_time.humanize()


def find_ts_units(ts):
    """Check units of unix time possibly?"""
    if len(ts) == 13:
        unit = "ms"
    elif len(ts) == 10:
        unit = "s"
    return unit


def string_to_datetime(date: str) -> datetime:
    """Convert string into a datetime object."""

    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


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


def check_ts_units(unix_ts):
    """Check if linux timestamp units are in seconds or ms."""

    if len(unix_ts) == 13:
        unit = "ms"
    elif len(unix_ts) == 10:
        unit = "s"
    return unit


def rm_col_names(_df, exclude_list):
    """Take dataframe column names and remove those in supplied exclude use."""

    col_names = list(_df.columns.values)
    for excl_str in exclude_list:
        try:
            col_names.remove(excl_str)
        except KeyError:
            pass

    return col_names


def drop_cols(_df, drop_list):
    """Drop columns from dataframe supplied in drop_list."""

    try:
        _df.drop(drop_list, axis=1, inplace=True)
    except ValueError:
        pass

    return _df


def read_data_sim(infile):
    """Read simulation csv file."""

    sim_ts_data = pd.read_csv(infile, sep=",", header=0)

    return sim_ts_data


def slice_dataframe(_df, start, finish):
    """Prob deprecated."""

    sliced = _df[start:finish].copy()
    slice_timestamp = unixtime_to_datetime(sliced["binned_ts"].iloc[0])

    return (sliced, slice_timestamp)


def slice_dataframe2(_df, start, finish):
    """Slice simulation dataframe into windowed segments."""

    sliced = _df[start:finish].copy()

    return sliced


def get_segment_1st_ts(unix_ts):
    """Slice simulation dataframe into windowed segments."""

    if len(str(unix_ts)) == 13:
        formatted_ts = unix_ts // 1000
    elif len(str(unix_ts)) == 10:
        formatted_ts = unix_ts

    first_timestamp = unixtime_to_datetime(formatted_ts)

    return first_timestamp


def delfiles_not_in_list(folder, exclude_list):
    """Delete all files in folder aprt from those in exclude list."""

    ### prepare delete list
    del_files = os.listdir(folder)
    # TODO: this is repeated in rm_col_names (generalise)
    for excl_str in exclude_list:
        try:
            del_files.remove(excl_str)
        except (ValueError, KeyError):
            pass

    ### delete files
    for rmfile in del_files:
        file_path = os.path.join(folder, rmfile)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as err:
            print(err)
    return
