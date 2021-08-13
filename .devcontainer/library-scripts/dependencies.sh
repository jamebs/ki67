#!/usr/bin/env bash
#
# Install base dependencies
#
# Syntax: ./dependencies.sh

set -e

echo "Installing conda dependencies..."
conda install -yq \
    'fastparquet=0.5.*' \
    'ipykernel=5.4.*' \
    'ipywidgets=7.6.*' \
    'matplotlib-base=3.3.*' \
    'numpy=1.19.*' \
    'pandas=1.2.*' \
    'pycodestyle=2.6.*' \
    'pydocstyle=5.1.*' \
    'pyyaml=5.4.*' \
    'scikit-image=0.15.*' \
    'scikit-learn=0.24.*' \
    'seaborn=0.11.*' \
    'scipy=1.6.*' \
    'tqdm=4.59.*'

echo "Installing pip dependencies..."
pip install --no-cache-dir \
    'tensorflow==2.4' \
    'https://github.com/NeuroSYS-pl/magda/archive/25abec214ff7c6969df2ec199f6f7cec108efcca.zip'

conda clean --all -fyq
