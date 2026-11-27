from pymongo import MongoClient
from pymongo.database import Database

from app.config import MONGODB_DB_NAME, MONGODB_URI


_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, tz_aware=True)
    return _client


def get_db() -> Database:
    return get_client()[MONGODB_DB_NAME]


def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None