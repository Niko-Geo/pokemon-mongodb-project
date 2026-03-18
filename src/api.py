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


def fetch_pokemon_batch(limit: int = 5, offset: int = 0) -> list[dict[str, Any]]:
    """
    Fetch a small batch of full Pokémon detail documents.

    If one Pokémon detail request fails, log the error and continue.
    """
    pokemon_refs = fetch_pokemon_list(limit=limit, offset=offset)
    pokemon_details: list[dict[str, Any]] = []

    for index, pokemon in enumerate(pokemon_refs, start=1):
        pokemon_name = pokemon.get("name", "unknown")
        pokemon_url = pokemon.get("url")

        print(f"[API] Fetching {index}/{len(pokemon_refs)}: {pokemon_name}")

        if not pokemon_url:
            print(f"[API][WARN] Missing URL for Pokémon: {pokemon_name}")
            continue

        try:
            detail = fetch_pokemon_detail(pokemon_url)
            pokemon_details.append(detail)
        except requests.RequestException as exc:
            print(f"[API][WARN] Request failed for {pokemon_name}: {exc}")
        except ValueError as exc:
            print(f"[API][WARN] Invalid payload for {pokemon_name}: {exc}")

    return pokemon_details
