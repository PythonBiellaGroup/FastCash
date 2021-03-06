FROM ubuntu:20.04

# Metadata
LABEL name="FastCash Dev Container"
LABEL maintainer="PythonBiellaGroup"
LABEL version="0.1"

ARG YOUR_ENV="venv"

# Install Node
#RUN apt-get update && apt-get install -y curl && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs

# Install Python
RUN apt-get update && apt-get install -y python3.8 python3-pip

# Install Git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

##########################
# Project Python definition
WORKDIR /fastcash

# Install Python libraries
ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"


#Copy all the project files
COPY . .

# Install project libraries
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry config virtualenvs.path $VENV_PATH
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project false
RUN poetry install --no-interaction --no-ansi


#Launch the main (if required)