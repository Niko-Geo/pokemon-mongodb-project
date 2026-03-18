from pymongo import MongoClient

from config import get_settings


def create_clean_collection() -> None:
    """
    Create the cleaned Pokémon collection from the raw collection
    using a MongoDB aggregation pipeline.
    """
    settings = get_settings()

    client = MongoClient(settings.mongo_uri)
    db = client[settings.database_name]
    raw_collection = db[settings.collection_raw]

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "name": 1,
                "height": 1,
                "weight": 1,
                "base_experience": 1,
                "types": {
                    "$map": {
                        "input": "$types",
                        "as": "type_item",
                        "in": "$$type_item.type.name",
                    }
                },
                "abilities": {
                    "$map": {
                        "input": "$abilities",
                        "as": "ability_item",
                        "in": "$$ability_item.ability.name",
                    }
                },
                "stats_object": {
                    "$arrayToObject": {
                        "$map": {
                            "input": "$stats",
                            "as": "stat_item",
                            "in": {
                                "k": "$$stat_item.stat.name",
                                "v": "$$stat_item.base_stat",
                            },
                        }
                    }
                },
            }
        },
        {
            "$project": {
                "id": 1,
                "name": 1,
                "height": 1,
                "weight": 1,
                "base_experience": 1,
                "types": 1,
                "abilities": 1,
                "hp": "$stats_object.hp",
                "attack": "$stats_object.attack",
                "defense": "$stats_object.defense",
                "special_attack": "$stats_object.special-attack",
                "special_defense": "$stats_object.special-defense",
                "speed": "$stats_object.speed",
                "total_stats": {
                    "$add": [
                        "$stats_object.hp",
                        "$stats_object.attack",
                        "$stats_object.defense",
                        "$stats_object.special-attack",
                        "$stats_object.special-defense",
                        "$stats_object.speed",
                    ]
                },
            }
        },
        {"$out": settings.collection_clean},
    ]

    raw_collection.aggregate(pipeline)
