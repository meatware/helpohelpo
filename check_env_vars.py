import os
import sys
import logging


def check_env_vars():
    """Check aws & github env variables required to run this script."""
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    # GITHUB_TOKEN = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    # GITHUB_TOKEN = ""

    if (AWS_ACCESS_KEY_ID is None) or (AWS_SECRET_ACCESS_KEY is None):
        LOG.critical("AWS access keys not set. Exiting..")
        sys.exit(0)
    LOG.info("AWS config good. Continuing...")
