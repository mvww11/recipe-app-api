FROM python:3.9-alpine3.13
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install lib that is prerequisites for running psycopg2
    apk add --update --no-cache postgresql-client && \
    # create virtual env with libs that are prerequisites for installing psycopg2
    # but not for running it. With this venv, we can easily delete those libs after installation
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    #install requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # (best practice) delete tmp folder para não pesar docker image
    rm -rf /tmp && \
    # remove the psycopg2 prerequisites that are necessairy for instalation
    # but not for execution. So we keep the docker image as lightweight as possible.
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user