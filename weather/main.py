from app.app import run_server
from loguru import logger


def serve():
    with run_server(50051) as (server, port):
        logger.info(f"Server is listening at port :{port}")
        server.wait_for_termination()


if __name__ == "__main__":
    serve()


# python3 -m grpc_tools.protoc -I ../protobufs/ --python_out=./ --grpc_python_out=./ ../protobufs/weather.proto