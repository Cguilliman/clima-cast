from dotenv import load_dotenv
import os
from pathlib import Path
from distutils.util import strtobool

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


MONGO_LINKS = os.environ.get("MONGO_LINKS", "mongodb://localhost:27017/")
MONGO_DB = os.environ.get("MONGO_DB", "")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "weather")

ELASTIC_HOST = os.environ.get("ELASTIC_HOST", "localhost")
ELASTIC_PORT = int(os.environ.get("ELASTIC_PORT", 9200))
ELASTIC_USER_SSL = bool(strtobool(os.environ.get("ELASTIC_USER_SSL", "False")))
