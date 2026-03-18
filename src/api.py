from typing import Any

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def fetch_pokemon_list(limit: int = 5, offset: int = 0) -> list[dict[str, Any]]:
    """
    Fetch a paginated list of Pokémon references from PokeAPI.

    Each item contains:
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


def fetch_pokemon_detail(url: str) -> dict[str, Any]:
    """
    Fetch the full detail document for one Pokémon from its detail URL.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    payload: dict[str, Any] = response.json()

    if "id" not in payload or "name" not in payload:
        raise ValueError(
            "Pokémon detail payload is missing required keys: 'id' or 'name'."
        )

    return payload


if __name__ == "__main__":
    pokemon_list = fetch_pokemon_list(limit=1, offset=0)
    first_pokemon = pokemon_list[0]

    print("List result:")
    print(first_pokemon)

    detail = fetch_pokemon_detail(first_pokemon["url"])

    print("\nDetail result:")
    print(f"id: {detail['id']}")
    print(f"name: {detail['name']}")
    print(f"height: {detail['height']}")
    print(f"weight: {detail['weight']}")
