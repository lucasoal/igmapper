rm -rf dist
rm -rf igmapper.egg-info
python -m build
python -m twine upload dist/* --verbose