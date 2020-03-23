#!/bin/bash

pdoc --html --force helpers --template-dir docs/custom_pdoc_templates/

echo -e "\nCopying Pdoc html"
cp -v html/helpers/*.html docs/

echo -e "\nCopying Coverage html"
cp -rfv htmlcov docs/

git add docs/*.html

echo -e "\n Please push documentation changes to repo"
