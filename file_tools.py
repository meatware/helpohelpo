import json


def _find_my_yamls(myc_folder, specific_files=None):
    """Load all .yaml files in a folder or a specific list of yaml files."""

    selected_files = []
    if specific_files:
        yaml_list = specific_files.replace(" ", "").split(",")
        all_files = [myc_folder + yaml for yaml in yaml_list]
    else:
        all_files = glob.glob(myc_folder + "/*.yaml")

    return all_files


def string_list_writer(file_name, list_holder, mode=None):
    """Writes an outfile froim a list of strings."""

    if mode == None:
        mode = "w"

    with open(file_name, mode) as file:
        for line_str in list_holder:
            file.write(line_str + "\n")


def simple_text_writer(file_name, text, mode=None):
    """
    Writes an outfile froim a list of strings.
    Mode = r, w, etc str.
    """

    if mode == None:
        mode = "w"

    with open(file_name, mode) as file:
        file.write(text)


def load_local_json2(data_file):
    """Return data from compact json file on a line-by-line basis."""
    for line in data_file:
        json_thing = json.loads(line)

        return json_thing


def load_local_json_generator(data_file):
    """Return data from compact json file on a line-by-line basis. Generator"""
    for line in data_file:
        json_thing = json.loads(line)

        yield json_thing
