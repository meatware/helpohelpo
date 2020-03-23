#!/bin/bash

pdoc --html --force helpers --template-dir docs/custom_pdoc_templates/

cp -v html/helpers/*.html docs/

git add docs/*.html

echo -e "\n Please push documentation changes to repo"
