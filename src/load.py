from typing import Any

from pymongo import MongoClient

from config import get_settings


def get_collection() -> Any:
    """
    Create MongoDB connection and return collection.
    """
    settings = get_settings()

    client = MongoClient(settings.mongo_uri)
    db = client[settings.database_name]

    return db[settings.collection_raw]


def insert_one_document(document: dict[str, Any]) -> None:
    """
    Insert a single document into MongoDB.
    """
    collection = get_collection()
    collection.insert_one(document)


def ensure_indexes() -> None:
    """
    Ensure required indexes exist.
    """
    collection = get_collection()
    collection.create_index("id", unique=True)


def insert_many_documents(documents: list[dict[str, Any]]) -> None:
    """
    Insert multiple documents into MongoDB.
    Ignores duplicates (based on unique index).
    """
    collection = get_collection()

    if not documents:
        return

    try:
        collection.insert_many(documents, ordered=False)
    except Exception as e:
        print(f"Insert warning: {e}")
