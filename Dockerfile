# Use dromni/nerfstudio:0.3.4 as the base image
FROM dromni/nerfstudio:main

# Set bash as the default shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash

# Change the user to root so that I don't need to use sudo
USER root

# Set up the requirements for using nerfstudio
RUN apt-get update && \
    apt-get install -y tree python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install nerfstudio

# These are extra packages that are not required for nerfstudio
RUN pip3 install jupyterlab ipywidgets mlflow psutil pynvml databricks-sdk

# Add the start.sh script to the container
ADD start.sh /

# Change the permissions of the start.sh script
RUN chmod +x /start.sh

# Define the command to run the start.sh script
CMD [ "/start.sh" ]
