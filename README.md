# [Assessment of Ki-67 proliferation index with deep learning in DCIS (ductal carcinoma in situ)](https://www.nature.com/articles/s41598-022-06555-3)

## Repository structure

1. `.devcontainer`\
Docker container specification and setup scripts
2. `.vscode`\
VS Code settings and recommended extensions
3. `data`\
Contains the input/output images and results
4. `ki67`\
Core python scripts of the presented solution
5. `notebooks`\
Jupyter Notebook containing model training
6. `main.py`\
Entry script

| The whole solution and experiments are built upon the [MAGDA :girl:](https://github.com/NeuroSYS-pl/magda) library |
|----|

Within the `ki67` folder you can find:
- `interfaces`\
  with *Data Transfer Objects* used by modules
- `modules`\
  with *single-responsibility* pieces of the solution, grouped by their logical roles
- `pipelines`\
  with YML configs describing the experiments/data flow and helper classes to run them
- `services`\
  helper classes used by the modules

The modules are combined into a pipeline depending on their purpose. You can find
pipelines in [ki67/pipelines/configs](ki67/pipelines/configs) directory.
You can run them with the `main.py` script.

## Quick Start

### Setup

Prerequisites:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### (a) Visual Studio Code

1. Open project in Visual Studio Code
2. Ensure you have installed [Remote Development Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) (`ms-vscode-remote.vscode-remote-extensionpack`)
3. Type command (`F1`): `Remote-Containers: Reopen in Container` (the docker container will be created according to [devcontainer specification](.devcontainer/devcontainer.json))

#### (b) Manual

1. Make sure you have installed `Python 3.7` and `pip`.
2. Install all dependencies listed in [requirements.txt](requirements.txt).

| ⚠️ The prepared `.devcontainer` doesn't work with GPU ⚠️ |
|---|
| Install dependencies manually or run the repository within the [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda) container to enable GPU(s) |

### Preparing data

Move your data to the specific folders:

**Example files structure BEFORE performing experiments**
```
┌ data
├─┬ experiments
│ └── config.json
├── results
└─┬ source
  ├── img-001.png
  ├── img-001.xml
  ├── ...
  ├── ...
  ├── img-095.png
  └── img-095.xml
```

The `source` directory should contain all slides (pROI saved as `.png` files) and correspoding markers (exported by ImageJ to `.xml` files). The config file splits images into chunks, e.g.

**config.json**
```json
{
  "testing": ["img-003", ... "img-094"],
  "shards": {
    "amy": ["img-001", ... "img-058"],
    "ben": ["img-002", ... "img-026"],
    "charlie": ["img-005", ... "img-013"]
  }
}
```

After performing training (each model is saved within the `data/experiments` directory) and evaluating the source images (all results are saved within the corresponding directories in `data/results`) the files structures should look like:

**Example files structure AFTER training and experiments**
```
┌ data
├─┬ experiments
│ ├─┬ densenet121-f48-s48-m0
│ │ ├─┬ amy
│ │ │ └─┬ weights.hdf5
│ │ │   └ ...
│ │ ├─┬ ben
│ │ │ └─┬ weights.hdf5
│ │ │   └ ...
│ │ └─┬ charlie
│ │   └─┬ weights.hdf5
│ │     └ ...
│ └── config.json
│
├─┬ results
│ ├─┬ img-001
│ │ └── ...
│ ├── ...
│ └─┬ img-095
│   └── ...
│
└─┬ source
  ├── img-001.png
  ├── img-001.xml
  ├── ...
  ├── ...
  ├── img-095.png
  └── img-095.xml
```

| 💡 In case of different data format 💡 |
|---|
| You can modify and combine modules into a new pipelines to adjust the solution to your data format. |

### Running solution

You can run solution through `main.py` which invokes the pipelines. Please note that
some pipelines should be run **before** and some **after training**. You can find
the appropriate comments within the script.

## License

The source code within this repository is distributed under the [Apache-2.0 License](LICENSE).
