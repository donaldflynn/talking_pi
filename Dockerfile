# Use the official Ubuntu 20.04 LTS image as the base image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Update apt packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    alsa-base \
    alsa-utils \
    nano \
    && rm -rf /var/lib/apt/lists/*


# Copy all files into /app in the container - including the requirements.txt
COPY . .


# Install the Python packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Share the audio devices with the container - use USB audio
RUN echo "defaults.pcm.card 3\ndefaults.ctl.card 3" > /etc/asound.conf

# Set permissions for audio devices
RUN usermod -aG audio root
