"""Helpers to manipulate dataframes"""

import os
from datetime import datetime
import pandas as pd

from helpers.date_tools import unixtime_to_datetime
import os
from datetime import datetime
import pandas as pd


def string_to_datetime(date: str) -> datetime:
    """Convert string into a datetime object."""

    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def unixtime_to_datestring(unix_time):
    """Convert unix timestamp into a string."""

    return datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")


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


def set_time_as_index(_df):
    """Set time column as dataframe index and then drop said column."""
    _df["time"] = pd.to_datetime(_df["time"], format="%H:%M:%S").dt.time
    _df.index = _df["time"]
    _df.drop(["time"], axis=1, inplace=True)
    return _df


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
    """Copy a df segment from df[x:y]."""

    sliced = _df[start:finish].copy()

    return sliced


# def get_segment_1st_ts(unix_ts):
#     """Slice simulation dataframe into windowed segments."""

#     if len(str(unix_ts)) == 13:
#         formatted_ts = unix_ts // 1000
#     elif len(str(unix_ts)) == 10:
#         formatted_ts = unix_ts

#     first_timestamp = unixtime_to_datetime(formatted_ts)

#     return first_timestamp
