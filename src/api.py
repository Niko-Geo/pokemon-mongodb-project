from typing import Any

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def fetch_pokemon_list(limit: int = 5, offset: int = 0) -> list[dict[str, Any]]:
    """
    Fetch a paginated list of Pokémon references from PokeAPI.

    Each item in the returned list contains:
    - name
    - url
    """
    response = requests.get(
        BASE_URL,
        params={"limit": limit, "offset": offset},
        timeout=30,
    )
    response.raise_for_status()

    payload: dict[str, Any] = response.json()
    results = payload.get("results", [])

    if not isinstance(results, list):
        raise ValueError("Expected 'results' to be a list.")

    return results


if __name__ == "__main__":
    pokemon = fetch_pokemon_list(limit=5, offset=0)
    for item in pokemon:
        print(item["name"], "->", item["url"])
