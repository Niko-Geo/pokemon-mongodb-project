import os
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient


def get_collection() -> Any:
    """
    Create MongoDB connection and return collection.
    """
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DATABASE_NAME")
    collection_name = os.getenv("COLLECTION_RAW")

    if not mongo_uri or not db_name or not collection_name:
        raise ValueError("Missing environment variables.")

    client = MongoClient(mongo_uri)
    db = client[db_name]

    return db[collection_name]


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
