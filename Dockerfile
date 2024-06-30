FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

ARG DB_PASSWORD
ARG DB_USERNAME
ARG DB_HOST
ARG DB_NAME
ARG SECRET_KEY

ENV DB_PASSWORD=${DB_PASSWORD} \
    DB_USERNAME=${DB_USERNAME} \
    DB_USERNAME=${DB_HOST} \
    DB_NAME=${DB_NAME} \
    SECRET_KEY=${SECRET_KEY} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . /app

EXPOSE 5000

CMD ["python3", "manage.py", "--host=0.0.0.0"]