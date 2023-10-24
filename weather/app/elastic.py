from elasticsearch_dsl import connections
from app import settings


def init_connection():
    connections.create_connection(
        hosts=[
            {
                "host": settings.ELASTIC_HOST,
                "port": settings.ELASTIC_PORT,
                "use_ssl": settings.ELASTIC_USER_SSL,
            }
        ],
    )
