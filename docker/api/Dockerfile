ARG PYTHON_VERSION=3.10-slim-bullseye
FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    build-essential
COPY ./requirements.txt .
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}
WORKDIR ${APP_HOME}
RUN apt-get update && apt-get install --no-install-recommends -y  \
    libpq-dev gettext curl postgresql \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/

COPY ./docker/api/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/api/background_worker/start /start_worker
RUN sed -i 's/\r$//g' /start_worker
RUN chmod +x /start_worker

COPY . ${APP_HOME}
ENTRYPOINT ["/entrypoint"]