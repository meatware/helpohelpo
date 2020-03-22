
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

def stringify_values(inlist):
    """Converts all items in dictionary key into strings."""

    string_items = []
    for item in inlist:
        if isinstance(item, dict):
            new_item = " ".join("{} {},".format(key, val) for key, val in item.items())
            string_items.append(new_item)
        elif isinstance(item, int):
            new_item = str(item)
            string_items.append(new_item)
        elif isinstance(item, str):
            string_items.append(item)
        else:
            LOG.error(
                "failed stringify item is %s, type: %s",
                item,
                type(item))
            raise Exception("failed stringify item is ", item, type(item))
    return string_items