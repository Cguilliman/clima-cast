from pymongo import MongoClient
from pymongo.collection import Collection
from app import settings


__all__ = ("client", "collection")


client = MongoClient(settings.MONGO_LINKS)
collection: Collection = client[settings.MONGO_DB][settings.MONGO_COLLECTION]
collection.create_index("capital.name")
