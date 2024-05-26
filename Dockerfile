FROM python:3.12 as builder

WORKDIR /app

COPY pyproject.toml ./

ENV POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

COPY ./src /app/src

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "-m", "src"]