FROM tiangolo/uvicorn-gunicorn:python3.10-slim

ENV  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PATH=/root/.local/bin:$PATH

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  python3-setuptools \ 
  bash \
  build-essential \
  python3-dev \
  curl \
  make \
  gettext \
  git \
  libpq-dev \
  wget \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false

WORKDIR /code

RUN poetry install --no-root

COPY .  /code/

