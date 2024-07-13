FROM python:3.8

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY pyproject.toml .

RUN pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

RUN chmod a+x test_task_ns/scripts_for_docker/*.sh