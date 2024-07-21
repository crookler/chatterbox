FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# Additional steps needed for pyaudio installation
RUN sudo apt-get update \
    && pip3 install --upgrade pip setuptools wheel \
    && sudo apt-get install portaudio19-dev -y

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt
