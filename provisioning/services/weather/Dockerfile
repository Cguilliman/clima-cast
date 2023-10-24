FROM python:3.11.4

RUN mkdir /service
COPY ./weather/pyproject.toml ./weather/poetry.lock /service/app/
COPY protobufs/ /service/protobufs/
COPY ./weather/ /service/app/
WORKDIR /service/app

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

RUN python -m grpc_tools.protoc -I /service/protobufs/ --python_out=/service/app/ --grpc_python_out=/service/app /service/protobufs/weather.proto

EXPOSE 50051
ENTRYPOINT ["python", "main.py"]
