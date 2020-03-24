#!/bin/bash -e

# pdoc --html --force helpers --template-dir docs/custom_pdoc_templates/

# echo -e "\nCopying Pdoc html"
# cp -v html/helpers/*.html docs/

# echo -e "\nCopying Coverage html"
# cp -rfv htmlcov docs/

# git add docs/*.html




portray as_html  --output_dir psite_temp --overwrite True 
cp -rf psite_temp/* docs/
cp -v  custom_css2/extra.css docs/css/extra.css
cp -v  custom_css2/favicon.ico docs/img/favicon.ico

cd docs/
rm *.sh *.txt 
cd -


git add docs/*

echo -e "\n Please push documentation changes to repo"