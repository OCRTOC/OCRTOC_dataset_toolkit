# OCRTOC Dataset Toolkit

Python toolkit for OCRTOC dataset.

## Installation
```bash
git clone https://github.com/OCRTOC/OCRTOC_dataset_toolkit.git
cd OCRTOC_dataset_toolkit
pip install .
# python3 is supported, python2 is not tested.
```

## Dataset Preparation
Download the dataset.

```bash
bash download.sh YOUR_DATASET_ROOT
```

The dataset file structure is shown in structure.txt

## Examples
Here are two examples on how to use this dataset toolkit.

```bash
cd examples

python example_loaddata.py --dataset_root YOUR_DATASET_ROOT

python example_vis_6dpose.py --dataset_root YOUR_DATASET_ROOT
```

## Documentations

We also provide detailed documentations for the toolkit. You can refer to the documentations for more details.
The documentation is available [here](https://ocrtoc-dataset-toolkit.readthedocs.io/en/latest/).

You can also build the documentation locally by running the following command.

```bash
cd OCRTOC_dataset_toolkit/docs
pip install -r requirements.txt
bash build_doc.sh
```

The documentation will be generated in [`docs/build/html`](/docs/build/html) folder. You can open [`index.html`](/docs/build/html/index.html) in the browser to see the documentations.
