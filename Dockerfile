# Use the official Ubuntu 22.04 LTS image as the base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Update apt packages and install necessary dependencies
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y \
    python3 \
    python3-pip \
    alsa-base \
    alsa-utils \
    ffmpeg \
    nano \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements.txt first to make use of caching
COPY requirements.txt requirements.txt

# Install the Python packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Share the audio devices with the container - use USB audio
RUN echo "defaults.pcm.card 3\ndefaults.ctl.card 3" > /etc/asound.conf

# Set permissions for audio devices
RUN usermod -aG audio root
