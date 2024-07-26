FROM python:3.9-alpine3.13
LABEL maintainer="adityamysore002@gmail.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 9000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib-dev zlib  && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        app-user && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app-user:app-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"
USER app-user
