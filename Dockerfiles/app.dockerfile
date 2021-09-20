FROM python:3.8-slim-buster

# Metadata
LABEL name="FastCash"
LABEL maintainer="PythonBiellaGroup"
LABEL version="0.1"

ARG YOUR_ENV="venv"

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

##########################
# Project Python definition
WORKDIR /admin-app

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
COPY pyproject.toml .
#COPY poetry.lock .
COPY /app ./app
COPY .env .
COPY launch.sh .

# Install project libraries
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false
RUN poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi


#Launch the main (if required)
RUN chmod +x launch.sh
CMD ["bash", "launch.sh"]