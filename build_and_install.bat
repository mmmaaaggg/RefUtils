python setup.py sdist bdist_wheel
cd dist 
pip uninstall ref_utils -y
pip install ref_utils-0.1-py3-none-any.whl
cd ..
