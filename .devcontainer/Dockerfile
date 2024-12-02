# Use the miniconda devcontainer image as the base image
FROM mcr.microsoft.com/devcontainers/python:latest

RUN apt-get update --yes && apt-get install --yes \
    bzip2 \
    bash \
    curl \
    wget \
    git \
    unzip \
    vim \
    nano \
    nodejs \
    yarn \
    openssl \
    gcc \
    musl-dev \
    libffi-dev \
    make

# Environment variables
ENV PYTHONPATH="$PYTHONPATH:/workspace/backend"

# Set the working directory
WORKDIR /workspace

# copy workspace to container
COPY . .

CMD [ "bash" ]