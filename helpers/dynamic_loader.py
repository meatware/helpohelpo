import os
import sys
import logging
import inspect
import importlib

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def _get_def_files(dirname):
    files = [
        fil.replace(".py", "") for fil in os.listdir(dirname) if fil.startswith("test_")
    ]

    LOG.info("def files found: %s", files)

    return files


def _import_func_defs(graphdef_files):

    _modules = __import__("func_defs", globals(), locals(), graphdef_files, 0)

    _module_list = [
        (key, value)
        for key, value in inspect.getmembers(_modules)
        if inspect.ismodule(value)
    ]

    LOG.info("_module_list %s", _module_list)

    func_dict = {}
    for module_name, _ in _module_list:
        # print("*", module_name, val)
        mymodule = importlib.import_module("func_defs." + module_name)
        LOG.info(" module Loaded %s", mymodule.__name__)

        for oxo in inspect.getmembers(mymodule):
            # print("oxo", oxo)
            if inspect.isfunction(oxo[1]):
                # func_dict["function_name"] = function
                func_name = oxo[1].__name__
                LOG.info(" func_name %s", func_name)
                func_dict[func_name] = oxo[1]

    LOG.info("No of function defs: %s ", str(len(func_dict)))

    return func_dict


def load(dirname):
    _func_def_files = _get_def_files(dirname)
    return _import_func_defs(_func_def_files)
