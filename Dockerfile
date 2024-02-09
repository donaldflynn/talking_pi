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
    && rm -rf /var/lib/apt/lists/*
#
## Add the pulseaudio repository
#RUN apt-get update && \
#    apt-get install -y software-properties-common && \
#    add-apt-repository -y ppa:ubuntu-audio-dev/pulse-testing && \
#    apt-get update
#
## Install pulseaudio
#RUN apt-get install -y pulseaudio



# Copy all files into /app in the container - including the requirements.txt
COPY . .


# Install the Python packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy alsa configuration
COPY alsa_config/default.conf /etc/modprobe.d/default.conf
