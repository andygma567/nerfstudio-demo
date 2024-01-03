# Use dromni/nerfstudio:0.3.4 as the base image
FROM dromni/nerfstudio:0.3.4

# Set bash as the default shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash

# Change the user to root
USER root

# Update the package lists
RUN apt-get update

# Install tree
RUN apt-get install -y tree

# Install pip
RUN apt-get install -y python3-pip

# Upgrade pip to the latest version
RUN pip3 install --no-cache-dir --upgrade pip

# Uninstall torch, torchvision, functorch, and tiny-cuda-nn
RUN pip3 uninstall -y torch torchvision functorch tinycudann

# Reinstall specific versions of torch and torchvision
# This specific version is needed to run the nerfstudio 
# according to the instructions in their docs. 
RUN pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# Install JupyterLab
RUN pip3 install jupyterlab

# Install ipywidgets
RUN pip3 install ipywidgets

# Install nerfstudio
RUN pip3 install nerfstudio

# Install mlflow libraries
RUN pip3 install mlflow psutil pynvml databricks-sdk

# Add the start.sh script to the container
ADD start.sh /

# Change the permissions of the start.sh script
RUN chmod +x /start.sh

# Define the command to run the start.sh script
CMD [ "/start.sh" ]
