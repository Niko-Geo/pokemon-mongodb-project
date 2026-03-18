import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    mongo_uri: str
    database_name: str
    collection_raw: str
    collection_clean: str
    api_limit: int
    api_offset: int


def get_settings() -> Settings:
    """
    Load configuration from environment variables.
    """
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    database_name = os.getenv("DATABASE_NAME")
    collection_raw = os.getenv("COLLECTION_RAW")
    collection_clean = os.getenv("COLLECTION_CLEAN")

    if not mongo_uri or not database_name or not collection_raw or not collection_clean:
        raise ValueError("Missing required environment variables.")

    api_limit = int(os.getenv("API_LIMIT", "5"))
    api_offset = int(os.getenv("API_OFFSET", "0"))

    return Settings(
        mongo_uri=mongo_uri,
        database_name=database_name,
        collection_raw=collection_raw,
        collection_clean=collection_clean,
        api_limit=api_limit,
        api_offset=api_offset,
    )
