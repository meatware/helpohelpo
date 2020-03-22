"""Python helpers module."""

import os
import sys
import logging
import shutil

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def delete_file(file_name):
    """Deletes a file from disk."""

    try:
        os.remove(file_name)
        LOG.info("Log file %s deleted from local drive", file_name)
    except OSError as err:
        LOG.warning("Log file %s does not exist %s", file_name, err)


def rm_dir_if_exists(target):
    """Remove file directory if it exists."""
    if os.path.exists(target):
        shutil.rmtree(target)


def rm_fil_if_exists(target):
    #  so we should check if file exists or not not before deleting them
    if os.path.exists(target):
        os.remove(target)
    else:
        LOG.warning("Delete file attempt failed for %s", target)


def copy_clobber(source, target):
    """Copy directory. Overwrite target folder if it exists."""

    rm_dir_if_exists(target)

    shutil.copytree(source, target)
    LOG.info("Copied: %s --> %s", source, target)


def select_os_things(my_wd="./", mode="file", suf_pre="", exclude_list=[]):
    """
    Create a filtered list of os type items.
    Mode can be folder, file, suffix, prefix.
    """

    if mode == "folder":
        os_thing_list = [
            thing
            for thing in os.listdir(my_wd)
            if os.path.isdir(thing)
            if thing not in exclude_list
        ]
    elif mode == "file":
        os_thing_list = [
            thing
            for thing in os.listdir(my_wd)
            if os.path.isfile(thing)
            if thing not in exclude_list
        ]
    elif mode == "suffix":
        os_thing_list = [
            thing
            for thing in os.listdir(my_wd)
            if thing.endswith(suf_pre)
            if thing not in exclude_list
        ]
    elif mode == "prefix":
        os_thing_list = [
            thing
            for thing in os.listdir(my_wd)
            if thing.startswith(suf_pre)
            if thing not in exclude_list
        ]
    else:
        LOG.critical("Incorrect mode: %s", mode)
        sys.exit(0)

    return os_thing_list


def count_str_whitespace(mystr):
    """Counts no of whitespace in string and returns an int."""
    count = 0
    for mychar in mystr:
        if mychar.isspace():
            count += 1
    return count


def unify_dic_key(key):
    unifiedkey = key.replace("_", "").replace("-", "").lower()

    return unifiedkey


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
