# Ki67 Proliferation Index

## Repository structure

1. `.devcontainer`\
Docker container specification and setup scripts
2. `.vscode`\
VSCode settings and recommended extensions
3. `data`\
Contains the input/output images and results
4. `ki67`\
Core python scripts of the presented solution
5. `notebooks`\
Jupyter Notebooks containing performed experiments

| The whole solution and experiments are built with the [MAGDA :girl:](https://github.com/NeuroSYS-pl/magda) library |
|----|
| You can find many modules performing a single action on the data. These modules are combined into a pipeline depending on the purpose. The pipelines' config you can find in [ki67/pipelines/configs](ki67/pipelines/configs) directory. |

## Quick Start

| Prerequisites |
|---|
| [Docker](https://www.docker.com/) |
| [Docker Compose](https://docs.docker.com/compose/install/) |
| [Nvidia Docker](https://github.com/NVIDIA/nvidia-docker) |

### (a) Visual Studio Code (recommended)

1. Open project in Visual Studio Code
2. Ensure you have installed [Remote Development Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) (`ms-vscode-remote.vscode-remote-extensionpack`)
3. Type command (`F1`): `Remote-Containers: Reopen in Container` (the docker container will be created according to [devcontainer specification](.devcontainer/devcontainer.json))

### (b) Docker

1. Run `docker-compose up -d --build` to build and start container
2. Attach to the created container
3. Each script/experiment/notebook should be run inside the container

### (c) Manual

1. Make sure you have installed [conda](https://docs.conda.io/en/latest/).
2. Install all dependencies listed in [the setup script](.devcontainer/library-scripts/dependencies.sh).

## Preparing data

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

The `source` directory contains all slides (pROI saved as `png` files) and correspoding markers (ImageJ export to `xml` files). The config file splits images into chunks, e.g.

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

After performing training (each models is saved within the `data/experiments` directory) and evaluating source images (all results are saved within the corresponding directories in `data/results`) the files structures should look like:

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

## License

The source code within this repository is distributed under the [Apache-2.0 License](LICENSE).
