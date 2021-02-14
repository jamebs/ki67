#!/usr/bin/env bash
#
# Script for installing and configuring MiniForge (Conda) and Python
#
# Syntax: ./miniforge.sh [conda path] [python version]

CONDA=${1:-"/opt/conda"}
PYTHON_VERSION=${2:-"3.8.6"}

CONDA_VERSION="4.9.2"
MINIFORGE_VERSION="${CONDA_VERSION}-5"
MINIFORGE_SHASUM="49dddb3998550e40adc904dae55b0a2aeeb0bd9fc4306869cc4a600ec4b8b47c"
export HOME=/home/$(id -un)

set -e

function updaterc() {
    echo -e "$1" | tee -a $HOME/.bashrc >> $HOME/.zshrc
}

cd $HOME
wget --quiet https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh
echo "${MINIFORGE_SHASUM} *Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" | sha256sum -c -
/bin/bash Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh -f -b -p $CONDA
rm Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh
updaterc "export PATH=${CONDA}/bin:\${PATH}"

${CONDA}/bin/conda config --system --set auto_update_conda false
${CONDA}/bin/conda config --system --set show_channel_urls true
${CONDA}/bin/conda config --set pip_interop_enabled true
${CONDA}/bin/conda install --quiet --yes python=$PYTHON_VERSION conda=${CONDA_VERSION} pip
${CONDA}/bin/conda update --all --quiet --yes
${CONDA}/bin/conda clean --all -f -y
