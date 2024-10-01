# Use the official Node.js image as a parent image
FROM mcr.microsoft.com/vscode/devcontainers/typescript-node:latest

# Install Yarn
RUN npm install -g yarn

# Set the working directory
WORKDIR /workspace

# Copy the current directory contents into the container at /workspace
COPY . /workspace

# Install project dependencies
RUN yarn install