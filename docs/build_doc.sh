rm source/ocrtoc_dataset_toolkit.*
rm source/modules.rst
pip install ..
sphinx-apidoc -o ./source ../ocrtoc_dataset_toolkit
make clean
make html
