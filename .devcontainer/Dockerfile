ARG CUDA_VERSION=11.0.3
ARG CUDNN_VERSION=8
ARG UBUNTU_VERSION=20.04
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-devel-ubuntu${UBUNTU_VERSION}

# [Option] Install zsh
ARG INSTALL_ZSH="true"
# [Option] Upgrade OS packages to their latest versions
ARG UPGRADE_PACKAGES="true"

# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
COPY .devcontainer/library-scripts/common-debian.sh /tmp/library-scripts/
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    && apt-get purge -y imagemagick imagemagick-6-common \
    # Install common packages, non-root user
    && bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

# Install MiniForge (Conda)
ARG CONDA=/opt/conda
# ARG PYTHON_VERSION=3.8.6
ARG PYTHON_VERSION=3.7.9
COPY .devcontainer/library-scripts/miniforge.sh /tmp/library-scripts/
RUN mkdir $CONDA && chown -R ${USER_UID}:${USER_GID} ${CONDA} \
    && su vscode -c "bash /tmp/library-scripts/miniforge.sh \"${CONDA}\" \"${PYTHON_VERSION}\"" \
    && rm -rf /tmp/library-scripts

# Install Dependencies
COPY .devcontainer/library-scripts/dependencies.sh /tmp/library-scripts/
RUN su vscode -c "export PATH=${CONDA}/bin:\${PATH} && bash /tmp/library-scripts/dependencies.sh" \
    && rm -rf /tmp/library-scripts

# Configure workspace
ENV APP=/workspace/ki67
RUN mkdir -p ${APP} && chown -R ${USER_UID}:${USER_GID} ${APP}

USER ${USERNAME}
ENTRYPOINT [ "/usr/bin/bash", "-c" ]
CMD [ "sleep infinity" ]
