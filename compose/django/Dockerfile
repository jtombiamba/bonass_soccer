ARG PYTHON_VERSION=3.13-slim-bookworm

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

ENV POETRY_PATH=/opt/poetry
ENV VENV_PATH=/opt/venv
ENV VENV_SITE_PACKAGES_PATH=${VENV_PATH}/lib/python3.11/site-packages
ENV VIRTUAL_ENV=${VENV_PATH}
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"
ENV PIP_NO_CACHE_DIR=on
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=30
# Python build stage
FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local
# ARG POETRY_OPTIONS=--no-dev
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Install apt packages
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  gcc \
  # postgres dependencies
  libpq-dev \
  curl \
  gettext \
  # PyGObject (pycairo) dependencies
  pkg-config \
  libcairo2-dev \
  libgirepository1.0-dev

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && python -m venv $VENV_PATH \
    && poetry config virtualenvs.create false \
    # cleanup
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VENV_PATH && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./poetry.lock ./pyproject.toml ./
# COPY ./requirements.txt /opt/app/requirements.txt
# COPY ./requirements.txt ./
# RUN pip install -r requirements.txt
RUN poetry install --no-root --no-interaction --no-ansi ${POETRY_OPTIONS}


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/opt/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Set user/group ID for avoiding permission issue - If no build-arg then using default value
ARG USER_ID=101
ARG GROUP_ID=101

RUN addgroup --gid ${GROUP_ID} --system django \
    && adduser --uid ${USER_ID} --no-create-home --disabled-password --system --ingroup django django \
    && apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y libpq-dev gettext libglib2.0-0 gir1.2-rsvg-2.0 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir ${APP_HOME} \
    && chown -R django:django ${APP_HOME}

WORKDIR ${APP_HOME}

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY --chown=django:django ./compose/${BUILD_ENVIRONMENT}/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY --chown=django:django --from=python-build-stage $VENV_PATH $VENV_PATH
COPY --chown=django:django . ${APP_HOME}
# COPY --chown=django:django ./sitecustomize.py $VENV_SITE_PACKAGES_PATH
USER django

RUN mkdir -p /opt/app/media
RUN mkdir -p /opt/app/staticfiles
RUN mkdir -p /opt/app/bonass_soccer/static

VOLUME ["/opt/app/media", "/opt/app/staticfiles"]

ENTRYPOINT ["/entrypoint"]
