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

# Install pip
RUN apt-get install -y python3-pip

# Install JupyterLab
RUN pip3 install jupyterlab

# Install ipywidgets
RUN pip3 install ipywidgets

# Add the start.sh script to the container
ADD start.sh /

# Change the permissions of the start.sh script
RUN chmod +x /start.sh

# Define the command to run the start.sh script
CMD [ "/start.sh" ]