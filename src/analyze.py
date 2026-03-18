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


def plot_top_10_strongest_pokemon() -> None:
    """
    Create a bar chart for the top 10 strongest Pokémon.
    """
    data = get_top_10_strongest_pokemon()

    names = [d["name"] for d in data]
    total_stats = [d["total_stats"] for d in data]

    plt.figure()
    plt.bar(names, total_stats)
    plt.xticks(rotation=45)
    plt.title("Top 10 Strongest Pokémon")
    plt.xlabel("Pokémon")
    plt.ylabel("Total Stats")

    plt.tight_layout()
    plt.savefig("images/top_10_strongest_pokemon.png")
    plt.close()


def get_total_stats_distribution() -> list[dict[str, Any]]:
    """
    Group Pokémon into total_stats ranges using MongoDB $bucket.
    """
    collection = get_clean_collection()

    pipeline = [
        {
            "$bucket": {
                "groupBy": "$total_stats",
                "boundaries": [0, 300, 400, 500, 600, 700],
                "default": "other",
                "output": {
                    "count": {"$sum": 1},
                },
            }
        },
        {"$sort": {"_id": 1}},
    ]

    return list(collection.aggregate(pipeline))


def plot_total_stats_distribution() -> None:
    """
    Create a bar chart for the distribution of total_stats buckets.
    """
    data = get_total_stats_distribution()

    labels = [str(item["_id"]) for item in data]
    counts = [item["count"] for item in data]

    plt.figure()
    plt.bar(labels, counts)
    plt.title("Distribution of Total Stats")
    plt.xlabel("Total Stats Range")
    plt.ylabel("Number of Pokémon")

    plt.tight_layout()
    plt.savefig("images/total_stats_distribution.png")
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

    plot_top_10_strongest_pokemon()
    print("Saved chart: images/top_10_strongest_pokemon.png")

    print("\nTotal stats distribution:\n")
    distribution = get_total_stats_distribution()
    for bucket in distribution:
        print(f"{bucket['_id']} | count={bucket['count']}")

    plot_total_stats_distribution()
    print("Saved chart: images/total_stats_distribution.png")
