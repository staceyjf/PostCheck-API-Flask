FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

ARG DB_PASSWORD
ARG DB_USERNAME
ARG DB_NAME
ARG DB_PORT
ARG DB_HOST
ARG SECRET_KEY

ENV DB_PASSWORD=${DB_PASSWORD} \
    DB_USERNAME=${DB_USERNAME} \
    DB_NAME=${DB_NAME} \
    DB_PORT=${DB_PORT} \
    DB_HOST=${DB_HOST} \
    SECRET_KEY=${SECRET_KEY} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade --no-cache-dir  pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "manage:app"]