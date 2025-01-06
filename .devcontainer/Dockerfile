FROM continuumio/miniconda3

ENV IS_DEV_CONTAINER=True

ARG INSTALL_UTILS=True

# Install snowflake cli
RUN apt update -y && \
    apt install pipx -y && \
    pipx ensurepath && \
    pipx install snowflake-cli


# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# Move container utilities package into container and install under user
COPY container_utils container_packages/container_utils/ 
RUN if [ "$INSTALL_UTILS" = "True" ]; then \
    /opt/conda/bin/pip install --user container_packages/container_utils/;\
    fi;

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
