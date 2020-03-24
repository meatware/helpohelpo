#!/bin/bash

python -m pytest --cov=helpers tests/
coverage html

# https://www.linuxjournal.com/content/python-testing-pytest-fixtures-and-coverage

