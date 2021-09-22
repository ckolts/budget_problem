FROM python:3.8-buster

WORKDIR /opt/src

COPY Pipfile Pipfile.lock /opt/src/

RUN pip install -U pip pipenv \
    && pipenv sync --dev

COPY wait-for-it /usr/local/bin/wait-for-it
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

