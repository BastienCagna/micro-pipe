rm -rf dist/
python3 -m pip install --upgrade twine
python3 -m pip install --upgrade build
python3 -m pip install --upgrade wheel
python3 -m build
twine upload --verbose dist/*