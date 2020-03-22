import json
from pprint import pprint
import sys
import collections


def find_nested_key(my_json, find_key):
    """Search in a nested dict for a key or None."""
    if find_key in my_json:
        return my_json[find_key]

    for _, vval in my_json.items():
        if isinstance(vval, dict):
            item = find_nested_key(vval, find_key)
            if item is not None:
                return item
    return None


def nested_dic_update(base_dic, in_dic):
    """ Recursively merge two nested dictionaries together."""
    for kkey, vval in in_dic.items():
        if isinstance(vval, collections.Mapping):
            recursive_call = nested_dic_update(base_dic.get(kkey, {}), vval)
            base_dic[kkey] = recursive_call
        else:
            base_dic[kkey] = in_dic[kkey]
    return base_dic


def find_replace_dict_values(mydict, search_key, old_value, new_value):
    "Recursively find and replace values in a nested dict"
    for key, val in mydict.items():
        if key == search_key:
            if val == old_value:
                mydict[key] = new_value
        elif isinstance(mydict[key], dict):
            find_replace_dict_values(mydict[key], search_key, old_value, new_value)
    return mydict
