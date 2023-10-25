from elasticsearch_dsl import connections
from app import settings
from loguru import logger


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
    conn = connections.get_connection()
    logger.info(conn)
    logger.info(conn.ping())
