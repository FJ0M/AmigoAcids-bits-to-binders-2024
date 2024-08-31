# DO NOT CHANGE
from 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main

workdir /tmp/docker-build/work/

shell [ \
    "/usr/bin/env", "bash", \
    "-o", "errexit", \
    "-o", "pipefail", \
    "-o", "nounset", \
    "-o", "verbose", \
    "-o", "errtrace", \
    "-O", "inherit_errexit", \
    "-O", "shift_verbose", \
    "-c" \
]
env TZ='Etc/UTC'
env LANG='en_US.UTF-8'

arg DEBIAN_FRONTEND=noninteractive

# Latch SDK
# DO NOT REMOVE
run pip install latch==2.39.5
run mkdir /opt/latch

# Install Mambaforge
run apt-get update --yes && \
    apt-get install --yes curl && \
    curl \
        --location \
        --fail \
        --remote-name \
        https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    `# Docs for -b and -p flags: https://docs.anaconda.com/anaconda/install/silent-mode/#linux-macos` \
    bash Mambaforge-Linux-x86_64.sh -b -p /opt/conda -u && \
    rm Mambaforge-Linux-x86_64.sh

# Set conda PATH
env PATH=/opt/conda/bin:$PATH
RUN conda config --set auto_activate_base false

# Build conda environment
copy environment.yml /opt/latch/environment.yaml
run mamba env create \
    --file /opt/latch/environment.yaml \
    --name SE3nv-cuda117
env PATH=/opt/conda/envs/SE3nv-cuda117/bin:$PATH


# Install packages manually 
RUN apt-get update --yes && \
    apt-get install --yes git
RUN pip install git+https://github.com/NVIDIA/dllogger#egg=dllogger
# RUN pip install "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
# RUN pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
RUN pip install --upgrade "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
# RUN pip install --upgrade jax jaxlib==0.3.14+cuda11.cudnn82 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

# Set the working directory
WORKDIR /RFdiffusion/env/SE3Transformer

# Install dependencies
COPY wf/RFdiffusion/env/SE3Transformer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the package
COPY wf/RFdiffusion/env/SE3Transformer/setup.py .
RUN python setup.py install

# Change back to the parent directory
# WORKDIR /RFdiffusion

# Install the package in editable mode
RUN pip install -e .

# Install additional system packages
USER root
RUN apt-get update && apt-get install -y aria2

# Trying to solve the error
RUN pip install --upgrade jax jaxlib flax

RUN pip install -U scikit-learn
RUN pip install tmtools

# Set environment variables
env BOWTIE2_INDEXES=reference

# Copy workflow data (use .dockerignore to skip files)
copy . /root/


# Latch workflow registration metadata
# DO NOT CHANGE
arg tag
# DO NOT CHANGE
env FLYTE_INTERNAL_IMAGE $tag

workdir /root
