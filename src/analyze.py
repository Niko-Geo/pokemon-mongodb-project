from typing import Any

from pymongo import MongoClient

from config import get_settings


def get_clean_collection() -> Any:
    """
    Return the cleaned Pokémon collection.
    """
    settings = get_settings()

    client = MongoClient(settings.mongo_uri)
    db = client[settings.database_name]

    return db[settings.collection_clean]


def get_top_10_strongest_pokemon() -> list[dict[str, Any]]:
    """
    Return the top 10 Pokémon by total_stats.
    """
    collection = get_clean_collection()

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "name": 1,
                "types": 1,
                "total_stats": 1,
            }
        },
        {"$sort": {"total_stats": -1, "id": 1}},
        {"$limit": 10},
    ]

    return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = get_top_10_strongest_pokemon()

    print("Top 10 strongest Pokémon:\n")

    for pokemon in results:
        print(
            f"{pokemon['name']} | "
            f"total_stats={pokemon['total_stats']} | "
            f"types={pokemon['types']}"
        )
