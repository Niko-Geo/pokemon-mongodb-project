from typing import Any

import matplotlib.pyplot as plt
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


def get_average_attack_by_type() -> list[dict[str, Any]]:
    """
    Compute average attack value per Pokémon type.
    """
    collection = get_clean_collection()

    pipeline = [
        {"$unwind": "$types"},
        {
            "$group": {
                "_id": "$types",
                "avg_attack": {"$avg": "$attack"},
                "count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "type": "$_id",
                "avg_attack": 1,
                "count": 1,
            }
        },
        {"$sort": {"avg_attack": -1}},
    ]

    return list(collection.aggregate(pipeline))


def plot_average_attack_by_type() -> None:
    """
    Create a bar chart of average attack per type.
    """
    data = get_average_attack_by_type()

    types = [d["type"] for d in data]
    avg_attack = [d["avg_attack"] for d in data]

    plt.figure()
    plt.bar(types, avg_attack)
    plt.xticks(rotation=45)
    plt.title("Average Attack by Pokémon Type")
    plt.xlabel("Type")
    plt.ylabel("Average Attack")

    plt.tight_layout()
    plt.savefig("images/avg_attack_by_type.png")
    plt.close()


if __name__ == "__main__":
    print("\nTop 10 strongest Pokémon:\n")
    strongest = get_top_10_strongest_pokemon()
    for p in strongest:
        print(f"{p['name']} | {p['total_stats']} | {p['types']}")

    print("\nAverage attack by type:\n")
    avg_attack = get_average_attack_by_type()
    for t in avg_attack:
        print(f"{t['type']} | avg_attack={t['avg_attack']:.2f} | n={t['count']}")

    plot_average_attack_by_type()
    print("\nSaved chart: images/avg_attack_by_type.png")
