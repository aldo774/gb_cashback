FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code


RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /code/

RUN poetry install --no-root --no-dev;

ADD . /code/

COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
